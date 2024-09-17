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
    # ui.input_action_button("classify_btn", "Classify"),
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
            # await asyncio.sleep(1)
            # await session.close()  # stops the server and ~ close the browser
            # return "Application has exited."
            return output_text

        words = input_str.split()

        if len(words) == 3 and all(word.isdigit() for word in words):
            sides = list(map(int, words))
            return classify_triangle(sides)
        else:
            return ""

    @output
    @render.text
    def error():
        input_str = input.input_string().strip()

        if input_str.lower().startswith(("exit", "quit")):
            return ""  # No error when exiting

        words = input_str.split()

        if len(words) == 0:
            return ""

        if len(words) != 3 or not all(word.isdigit() for word in words):
            if any(word.lower() in ["exit", "quit"] for word in words):
                return ""  # No error for exit or quit command
            if len(words) == 2:
                return "Error: One side missing"
            elif len(words) == 1:
                return "Error: Two sides missing"
            elif len(words) > 3:
                return "Error: Too many sides provided"
            else:
                return "Error: Non-numeric value encountered"
        return ""


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
