# -*- coding: utf-8 -*-

import os
import json
import numpy as np
import tensorflow as tf

import model, sample, encoder

class Conversation:
    """Simple Conversation class with two users, their nicks and the messages so
    far. This is dumb but enough for the purpose of this mini bot. It can output
    the conversation with double newlines for GPT-2 to take as input, add
    replies, and that's about it. """

    def __init__(self, name_human, name_computer):
        self.name_human = name_human
        self.name_computer = name_computer
        self.conversation = []

    def add(self, name, text):
        self.conversation.append("{}: {}".format(name, text))

    def add_computer(self, text):
        self.add(self.name_computer, text)

    def add_human(self, text):
        self.add(self.name_human, text)

    def text_generic(self, nspace = 1):
        output = ""
        for reply in self.conversation:
            output = output + (reply + ("\n" * nspace))
        return output

    def text_gpt(self):
        return self.text_generic(2)

def chat(model_name='117M', seed=None, length=50):

    # Prepare conversation and context
    conversation = Conversation("Hudson", "Jayme")
    conversation.add_human("Hi!")
    conversation.add_computer("Hey!")
    conversation.add_human("I'm a human named {}, who are you?".format(conversation.name_human))
    conversation.add_computer("I'm a computer program but refer to me as {} please".format(conversation.name_computer))
    conversation.add_human("How exciting! Are you ready to chat?")
    conversation.add_computer("Sure thing! You go first.")

    # Prepare the model
    enc = encoder.get_encoder(model_name)
    hparams = model.default_hparams()
    with open(os.path.join('models', model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length > hparams.n_ctx:
        raise ValueError("Can't get samples longer than window size: %s" % hparams.n_ctx)

    with tf.Session(graph=tf.Graph()) as sess:
        np.random.seed(seed)
        tf.set_random_seed(seed)
        context = tf.placeholder(tf.int32, [1, None])
        output = sample.sample_sequence(
                hparams=hparams, length=length, context=context, batch_size=1
                # temperature=temperature, top_k=top_k
                )

        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join('models', model_name))
        saver.restore(sess, ckpt)

        # Print the initial context/prompt
        print(conversation.text_generic(1))

        while True:

            # Let the human speak
            message = None
            while not message:
                message = input("{}: ".format(conversation.name_human))
            conversation.add_human(message)

            # Let the computer speak
            prompt = conversation.text_gpt() + "\n\n{}: ".format(conversation.name_computer)

            encoded_prompt = enc.encode(prompt)

            result= sess.run(output, feed_dict={
                context: [encoded_prompt]
                })[:, len(encoded_prompt):]
            text = enc.decode(result[0])

            reply = (text.split('\n'))[0]
            conversation.add_computer(reply)
            print("{}: {}".format(conversation.name_computer, reply))

if __name__ == '__main__':
    chat()
