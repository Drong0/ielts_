import openai
import re


class EssayEvaluator:
    def __init__(self):
        openai.api_key = "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"

    def evaluate_essay(self, header, essay):
        score_requirement_text = "I need you to score this essay from 1 to 10 as if you were an admission committee. Return only integer, no additional text. This is a hard requirement. Remove any lines such as \"as an AI model\""
        feedback_requirement_text = "I need you to provide 5 bullet points feedback. Return only python list"
        get_score_text = header + "\n" + "" + "\n" + score_requirement_text
        get_feedback_text = header + "\n" + essay + "\n" + feedback_requirement_text


        response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=get_score_text,
                temperature=0.5,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60
        )
        score = response.choices[0].text.strip()
        score = re.sub(r'[^0-9]', '', score)




        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=get_feedback_text,
                temperature=0.5,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60
            )
            feedback = response.choices[0].text.strip()
        except Exception as e:
            feedback = "We were not able to generate feedback for your essay"

        return score, feedback

    def evaluate_general_essay(self, topic, text):
        if not topic:
            topic = "General University Application essay"
        header = f"Please evaluate the following motivational essay. The topic is {topic}. "
        return self.evaluate_essay(header, text)

    def evaluate_university_specific_essay(self, topic, text, university):
        header = f"Please evaluate the following motivational essay. The topic is {topic}. Student is applying to {university}"
        return self.evaluate_essay(header, text)