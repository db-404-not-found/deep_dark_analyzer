from pathlib import Path
from time import sleep
from typing import Any

# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

PROJECT_PATH = Path("./backend")


class MultiFunctionalModel:
    def __init__(self) -> None:
        # self.cuda = torch.cuda.is_available()
        # self.train_dir = "train_output"
        # premodel = GPT2LMHeadModel.from_pretrained(
        #     PROJECT_PATH / self.train_dir, local_files_only=True
        # )
        # try:
        #     self.tok = GPT2Tokenizer.from_pretrained(PROJECT_PATH / self.train_dir)
        # except OSError as error:
        #     logger.exception("Upalo")
        #     raise error

        # self.model = premodel.to("cuda" if self.cuda else "cpu")
        # self.eot_token = "<|endoftext|>"
        # self.question_token = "<|Вопрос:|> "
        # self.answer_token = " <|Ответ:|> "
        # self.max_length = 64
        pass

    def predict(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        sleep(15)
        return {
            "estimation": "AAA",
            "indexes": [
                (0, 10),
                (100, 120),
            ],
        }
