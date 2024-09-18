from shiny import App, ui, reactive, render
import asyncio


def classify_triangle(sides):
    a, b, c = sorted(sides)

    if a + b <= c:
        return "No Triangle"
    elif a == b == c:
        return "Equilateral"
    elif a == b or b == c or a == c:
        return "Isosceles"
    else:
        return "Scalene"


app_ui = ui.page_fluid(
    ui.panel_title("Triangle Classifier"),
    ui.input_text("input_string", "Enter the sides of a triangle (separated by spaces):", ""),
    ui.output_text_verbatim("result"),
    ui.output_text_verbatim("error")
)


def server(input, output, session):
    @output
    @render.text
    async def result():
        input_str = input.input_string().strip()

        if input_str.lower().startswith(("exit", "quit")):
            output_text = "Application has exited."
            return output_text

        words = input_str.split()

        if len(words) == 3 and all(word.isdigit() or (word.startswith('-') and word[1:].isdigit()) for word in words):
            sides = list(map(int, words))
            return classify_triangle(sides)
        else:
            return ""

    @output
    @render.text
    def error():
        input_str = input.input_string().strip()

        if input_str.lower().startswith(("exit", "quit")):
            return ""

        words = input_str.split()

        if len(words) == 0:
            return ""

        # non numeric input check
        if not all(word.isdigit() or (word.startswith('-') and word[1:].isdigit()) for word in words):
            return "Error: Invalid input. Only numbers and the commands 'Quit' or 'Exit' are acceptable."

        # checking negative sides
        if any(word.startswith('-') and word[1:].isdigit() for word in words):
            return "Error: Triangles can't have negative sides"

        # check for invalid sides
        if len(words) != 3:
            if len(words) == 2:
                return "Error: One side missing"
            elif len(words) == 1:
                return "Error: Two sides missing"
            elif len(words) > 3:
                return "Error: Too many sides provided"

        return ""

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
