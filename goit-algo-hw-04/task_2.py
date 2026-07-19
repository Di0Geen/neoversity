import turtle


def koch_curve(t: turtle.Turtle, length: float, level: int) -> None:
    if level == 0:
        t.forward(length)
        return

    part = length / 3
    koch_curve(t, part, level - 1)
    t.left(60)
    koch_curve(t, part, level - 1)
    t.right(120)
    koch_curve(t, part, level - 1)
    t.left(60)
    koch_curve(t, part, level - 1)


def koch_snowflake(level: int, length: int = 300) -> None:
    screen = turtle.Screen()
    screen.title("Koch Snowflake")

    t = turtle.Turtle()
    t.speed(0)
    t.color("blue")
    t.penup()
    t.goto(-length / 2, length / 3)
    t.pendown()

    for _ in range(3):
        koch_curve(t, length, level)
        t.right(120)

    t.hideturtle()
    screen.mainloop()


def main() -> None:
    try:
        level = int(input("Enter recursion level: "))
        if level < 0:
            raise ValueError
    except ValueError:
        print("Please enter a non-negative integer.")
        return

    koch_snowflake(level)


if __name__ == "__main__":
    main()
