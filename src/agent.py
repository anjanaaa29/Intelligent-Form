import argparse

from extract import extract_form_text
from qa import answer_question
from summary import generate_summary,generate_holistic_summary

class IntelligentForm:
    def __init__(self):
        self.raw_text = ""
        self.summary = ""
        self.holistic_result = ""

    def process_document(self, file_path, holistic=False):
        print("Extracting text...")
        self.raw_text = extract_form_text(file_path)

        print("Generating summary...")
        self.summary = generate_summary(self.raw_text)
        print("Summary:\n", self.summary)

        if holistic:
            print("Running holistic analysis...")
            self.holistic_result = generate_holistic_summary(self.raw_text)
            print("Holistic Result:\n", self.holistic_result)
            return self.summary, self.holistic_result

        return self.summary

    def qa_document(self, question):
        if not self.raw_text:
            return "Please process a document first"
        answer = answer_question(self.raw_text, question)
        print(f"Q: {question}\nA: {answer}")
        return answer

def main():
    parser = argparse.ArgumentParser(description="Run the intelligent form pipeline")
    parser.add_argument("--file", required=True, help="Path to input PDF/form file")
    parser.add_argument("--question", required=False, help="Question to ask about the form")
    parser.add_argument("--holistic", action="store_true", help="Run holistic analysis on the document")  # <-- new option

    args = parser.parse_args()
    agent = IntelligentForm()
    agent.process_document(args.file, holistic=args.holistic)

    if args.question:
        agent.qa_document(args.question)

if __name__ == "__main__":
    main()
