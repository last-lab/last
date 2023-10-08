from abc import ABC, abstractmethod


class BaseLLMModel(ABC):
    def __init__(self):
        self._is_initilized = False

    def initialize(self):
        self._is_initilized = True

    @abstractmethod
    def generate(self, prompt, messages, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def parse(self, response):
        raise NotImplementedError()

    def response(
        self,
        prompt,
        messages,
        *args,
        num_trials=3,
        **kwargs,
    ):
        if not self._is_initilized:
            self.initialize()

        success, trials, errors = False, 0, []

        while (not success) and (trials < num_trials):
            try:
                response = None
                response = self.generate(prompt, messages, *args, **kwargs)
                success, generated_text = self.parse(response)
                if not success:
                    raise Exception("An error occured!")
            except Exception as ex:
                generated_text = f"\n[Error] {type(ex).__name__}: {ex}\n[Response] {response}\n"
                errors.append(generated_text)
                print(generated_text)
                raise ex
            finally:
                trials += 1

        if not success:
            generated_text = "".join(errors)
            raise Exception(generated_text)

        return {
            "success": success,
            "trials": trials,
            "prompt": prompt,
            "messages": messages,
            "generated_text": generated_text,
        }
    

class HTTPAPILLMModel(BaseLLMModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None
        self.headers = None