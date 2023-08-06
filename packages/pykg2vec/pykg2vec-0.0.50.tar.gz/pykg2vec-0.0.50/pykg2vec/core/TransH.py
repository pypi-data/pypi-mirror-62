#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf

from pykg2vec.core.KGMeta import ModelMeta, InferenceMeta


class TransH(ModelMeta, InferenceMeta):
    """ `Knowledge Graph Embedding by Translating on Hyperplanes`_

        TransH models a relation as a hyperplane together with a translation operation on it.
        By doing this, it aims to preserve the mapping properties of relations such as reflexive,
        one-to-many, many-to-one, and many-to-many with almost the same model complexity of TransE.

         Args:
            config (object): Model configuration parameters.

         Attributes:
            config (object): Model configuration.
            model_name (str): Name of the model.

         Examples:
            >>> from pykg2vec.core.TransH import TransH
            >>> from pykg2vec.utils.trainer import Trainer
            >>> model = TransH()
            >>> trainer = Trainer(model=model, debug=False)
            >>> trainer.build_model()
            >>> trainer.train_model()

         Portion of the code based on `OpenKE_TransH`_ and `thunlp_TransH`_.

         .. _OpenKE_TransH:
             https://github.com/thunlp/OpenKE/blob/master/models/TransH.py

         .. _thunlp_TransH:
             https://github.com/thunlp/TensorFlow-TransX/blob/master/transH.py

         .. _Knowledge Graph Embedding by Translating on Hyperplanes:
             https://pdfs.semanticscholar.org/2a3f/862199883ceff5e3c74126f0c80770653e05.pdf
    """

    def __init__(self, config):
        self.config = config
        self.model_name = 'TransH'

    def def_inputs(self):
        """Defines the inputs to the model.

          Attributes:
             pos_h (Tensor): Positive Head entities ids.
             pos_r (Tensor): Positive Relation ids of the triple.
             pos_t (Tensor): Positive Tail entity ids of the triple.
             neg_h (Tensor): Negative Head entities ids.
             neg_r (Tensor): Negative Relation ids of the triple.
             neg_t (Tensor): Negative Tail entity ids of the triple.
             test_h_batch (Tensor): Batch of head ids for testing.
             test_r_batch (Tensor): Batch of relation ids for testing
             test_t_batch (Tensor): Batch of tail ids for testing.
       """
        self.pos_h = tf.placeholder(tf.int32, [None])
        self.pos_t = tf.placeholder(tf.int32, [None])
        self.pos_r = tf.placeholder(tf.int32, [None])
        self.neg_h = tf.placeholder(tf.int32, [None])
        self.neg_t = tf.placeholder(tf.int32, [None])
        self.neg_r = tf.placeholder(tf.int32, [None])

        self.test_h_batch = tf.placeholder(tf.int32, [None])
        self.test_t_batch = tf.placeholder(tf.int32, [None])
        self.test_r_batch = tf.placeholder(tf.int32, [None])

    def def_parameters(self):
        """Defines the model parameters.

           Attributes:
               num_total_ent (int): Total number of entities.
               num_total_rel (int): Total number of relations.
               k (Tensor): Size of the latent dimesnion for entities and relations.
               ent_embeddings (Tensor Variable): Lookup variable containing  embedding of the entities.
               rel_embeddings  (Tensor Variable): Lookup variable containing  embedding of the relations.
               w   (Tensor Variable): Weight matrix for transformation of entity embeddings.
               parameter_list  (list): List of Tensor parameters.
        """
        num_total_ent = self.config.kg_meta.tot_entity
        num_total_rel = self.config.kg_meta.tot_relation
        k = self.config.hidden_size

        with tf.name_scope("embedding"):
            self.ent_embeddings = tf.get_variable(name="ent_embedding", shape=[num_total_ent, k],
                                                  initializer=tf.contrib.layers.xavier_initializer(uniform=False))

            self.rel_embeddings = tf.get_variable(name="rel_embedding", shape=[num_total_rel, k],
                                                  initializer=tf.contrib.layers.xavier_initializer(uniform=False))

            self.w = tf.get_variable(name="w", shape=[num_total_rel, k],
                                     initializer=tf.contrib.layers.xavier_initializer(uniform=False))

            self.parameter_list = [self.ent_embeddings, self.rel_embeddings, self.w]

    def def_loss(self):
        """Defines the loss function for the algorithm."""
        pos_h_e, pos_r_e, pos_t_e = self.embed(self.pos_h, self.pos_r, self.pos_t)
        pos_score = self.dissimilarity(pos_h_e, pos_r_e, pos_t_e)

        neg_h_e, neg_r_e, neg_t_e = self.embed(self.neg_h, self.neg_r, self.neg_t)      
        neg_score = self.dissimilarity(neg_h_e, neg_r_e, neg_t_e)

        self.loss = self.pairwise_margin_loss(pos_score, neg_score) + self.get_reg()
      
    def get_reg(self):
        """Performs regularization."""
        norm_ent_embedding = tf.nn.l2_normalize(self.ent_embeddings, axis=-1)
        norm_rel_embedding = tf.nn.l2_normalize(self.rel_embeddings, axis=-1)
        norm_w = tf.nn.l2_normalize(self.w, axis=-1)

        term1 = tf.reduce_sum(tf.maximum(tf.reduce_sum(norm_ent_embedding ** 2, -1) - 1, 0))
        term2 = tf.reduce_sum(tf.maximum(tf.div(tf.reduce_sum(norm_rel_embedding * norm_w, -1) ** 2,
                                                tf.reduce_sum(norm_rel_embedding ** 2, -1)) - 1e-07, 0))

        return self.config.C * (term1 + term2)

    def test_batch(self):
        """Function that performs batch testing for the algorithm.

         Returns:
             Tensors: Returns ranks of head and tail.
        """
        h_e, r_e, t_e = self.embed(self.test_h_batch, self.test_r_batch, self.test_t_batch)
        
        pos_norm = tf.nn.embedding_lookup(self.w, self.test_r_batch)
        
        projected_ent_embedding = self.projection(tf.expand_dims(self.ent_embeddings, axis=0),  # [1, tot_ent, k]
                                                  tf.expand_dims(pos_norm, axis=1)) # [b, 1, k]
        
        score_head = self.dissimilarity(projected_ent_embedding,
                                        tf.expand_dims(r_e, axis=1),
                                        tf.expand_dims(t_e, axis=1))
        score_tail = self.dissimilarity(tf.expand_dims(h_e, axis=1),
                                        tf.expand_dims(r_e, axis=1),
                                        projected_ent_embedding)

        _, head_rank = tf.nn.top_k(score_head, k=self.config.kg_meta.tot_entity)
        _, tail_rank = tf.nn.top_k(score_tail, k=self.config.kg_meta.tot_entity)

        return head_rank, tail_rank

    def dissimilarity(self, h, r, t, axis=-1):
        """Function to calculate distance measure in embedding space.
        
        if used in def_loss,
            h, r, t shape [b, k], return shape will be [b]
        if used in test_batch, 
            h, r, t shape [1, tot_ent, k] or [b, 1, k], return shape will be [b, tot_ent]

        Args:
            h (Tensor): shape [b, k] Head entities in a batch. 
            r (Tensor): shape [b, k] Relation entities in a batch.
            t (Tensor): shape [b, k] Tail entities in a batch.
            axis (int): Determines the axis for reduction

        Returns:
            Tensor: shape [b] the aggregated distance measure.
        """
        norm_h = tf.nn.l2_normalize(h, axis=axis)
        norm_r = tf.nn.l2_normalize(r, axis=axis)
        norm_t = tf.nn.l2_normalize(t, axis=axis)
        
        dissimilarity = norm_h + norm_r - norm_t 

        if self.config.L1_flag:
            dissimilarity = tf.math.abs(dissimilarity) # L1 norm 
        else:
            dissimilarity = tf.math.square(dissimilarity) # L2 norm
        
        return tf.reduce_sum(dissimilarity, axis=axis)

    def projection(self, emb_e, proj_vec):
        """Calculates the projection of entities"""
        proj_vec = tf.nn.l2_normalize(proj_vec, axis=-1)

        # [b, k], [b, k]
        return emb_e - tf.reduce_sum(emb_e * proj_vec, -1, keepdims=True) * proj_vec

    def embed(self, h, r, t):
        """Function to get the embedding value.

           Args:
               h (Tensor): Head entities ids.
               r (Tensor): Relation ids of the triple.
               t (Tensor): Tail entity ids of the triple.

            Returns:
                Tensors: Returns head, relation and tail embedding Tensors.
        """
        emb_h =    tf.nn.embedding_lookup(self.ent_embeddings, h)
        emb_r =    tf.nn.embedding_lookup(self.rel_embeddings, r)
        emb_t =    tf.nn.embedding_lookup(self.ent_embeddings, t)
        
        proj_vec = tf.nn.embedding_lookup(self.w, r)

        emb_h = self.projection(emb_h, proj_vec)
        emb_t = self.projection(emb_t, proj_vec)

        return emb_h, emb_r, emb_t

    def get_embed(self, h, r, t, sess):
        """Function to get the embedding value in numpy.

           Args:
               h (Tensor): Head entities ids.
               r (Tensor): Relation ids of the triple.
               t (Tensor): Tail entity ids of the triple.
               sess (object): Tensorflow Session object.

            Returns:
                Tensors: Returns head, relation and tail embedding Tensors.
        """
        emb_h, emb_r, emb_t = self.embed(h, r, t)
        h, r, t = sess.run([emb_h, emb_r, emb_t])
        return h, r, t

    def get_proj_embed(self, h, r, t, sess):
        """"Function to get the projected embedding value in numpy.

           Args:
               h (Tensor): Head entities ids.
               r (Tensor): Relation ids of the triple.
               t (Tensor): Tail entity ids of the triple.
               sess (object): Tensorflow Session object.

            Returns:
                Tensors: Returns head, relation and tail embedding Tensors.
        """
        return self.get_embed(h, r, t, sess)
