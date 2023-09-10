# !pip install transformers - обязательно


class CBRF:
    def __init__(self, savepath="."):
        from pathlib import Path

        import pandas as pd
        import tensorflow as tf
        from transformers import AutoModel, AutoTokenizer, MBartForConditionalGeneration

        self.savepath = Path(savepath) / "cbrf"

        AutoTokenizer.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")
        AutoModel.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")

        mmodel_name = "IlyaGusev/mbart_ru_sum_gazeta"
        AutoTokenizer.from_pretrained(mmodel_name)
        MBartForConditionalGeneration.from_pretrained(mmodel_name)

        loaded = False
        if self.savepath.exists():
            try:
                self.model = tf.keras.models.load_model(savepath)
                loaded = True
            except:
                pass
        if not loaded:
            mx_input = tf.keras.layers.Input((512, 1024))
            mx = tf.keras.layers.Flatten()(mx_input)
            mx = tf.keras.layers.Dense(256 * 2, activation="tanh")(mx)
            # mx = tf.keras.layers.Dropout(0.25)(mx)
            mx = tf.keras.layers.Dense(64 * 2, activation="tanh")(mx)
            # mx = tf.keras.layers.Dropout(0.25)(mx)
            mx_output = tf.keras.layers.Dense(
                17,
                activation="softmax",
                bias_regularizer=tf.keras.regularizers.L1L2(0.0, 0.1),
            )(mx)
            self.model = tf.keras.Model(inputs=mx_input, outputs=mx_output)

        ratings_list = ["AAA"]
        modified = ["AA", "A", "BBB", "BB", "B"]
        modifiers = ["+", "", "-"]
        unmodified = ["C"]
        categories_list = ratings_list + modified + unmodified
        for rating in modified:
            for suffix in modifiers:
                ratings_list.append(rating + suffix)
        ratings_list += unmodified
        category = [0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6]
        rating_values = [0, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 24]
        self.ratings = pd.DataFrame(
            {
                "values": rating_values,
                "class": list(range(len(ratings_list))),
                "category": category,
            },
            index=ratings_list,
        )
        self.categories = pd.DataFrame(
            {
                "values": [4 * i for i in range(7)],
                "class": list(range(len(categories_list))),
            },
            index=categories_list,
        )

    def number_to_rating(self, number):
        return self.ratings.iloc[number].name

    def number_to_category(self, number):
        cn = self.ratings.iloc[number].category
        return self.categories.iloc[cn].name

    def predict(self, release):
        """Возвращает число, который можно преобразовать в рейтинг number_to_rating
        или в категорию number_to_category
        """

        import torch
        from transformers import AutoModel, AutoTokenizer

        stokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")
        smodel = AutoModel.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")
        encoded_input = stokenizer(
            release, padding=True, truncation=True, max_length=512, return_tensors="pt"
        )
        with torch.no_grad():
            model_output = smodel(**encoded_input)
        res = self.model.predict(model_output[0].numpy())
        return res.argmax(axis=1)[0]

    def train(self, releases, ratings):
        import numpy as np
        import tensorflow as tf
        import torch
        from transformers import AutoModel, AutoTokenizer

        stokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")
        smodel = AutoModel.from_pretrained("ai-forever/sbert_large_mt_nlu_ru")
        outputs = []
        for release in releases:
            encoded_input = stokenizer(
                release,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            )
            with torch.no_grad():
                model_output = smodel(**encoded_input)
            outputs.append(model_output[0][0].numpy())
        outputs = np.array(outputs)

        numbers = []
        for rating in ratings:
            numbers.append(self.ratings["class"].loc[rating])
        numbers = np.array(numbers)

        batch_size = min(20, len(outputs))
        steps = len(outputs) / batch_size
        epochs = 10
        learning_rate = 1e-6
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
        )
        self.model.fit(
            outputs,
            numbers,
            epochs=epochs,
            steps_per_epoch=steps,
            batch_size=batch_size,
            # class_weight=class_weight,
            callbacks=[],
        )

        epochs = 20
        learning_rate = 1e-7
        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
        )
        history = self.model.fit(
            outputs,
            numbers,
            epochs=epochs,
            steps_per_epoch=steps,
            batch_size=batch_size,
            # class_weight=class_weight,
            callbacks=[],
        )

        self.model.save(self.savepath)
        return history.history

    def keywords(self, release):
        from transformers import AutoTokenizer, MBartForConditionalGeneration

        mmodel_name = "IlyaGusev/mbart_ru_sum_gazeta"
        mtokenizer = AutoTokenizer.from_pretrained(mmodel_name)
        mmodel = MBartForConditionalGeneration.from_pretrained(mmodel_name)

        input_ids = mtokenizer(
            [release],
            max_length=600,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )["input_ids"]

        output_ids = mmodel.generate(
            input_ids=input_ids,
            no_repeat_ngram_size=4,
            pad_token_id=1,
            eos_token_id=2,
        )[0]

        summary = mtokenizer.decode(output_ids, skip_special_tokens=True)
        sentences = summary.split(". ")
        words = sentences[1].split(" ")
        return words[:3]
