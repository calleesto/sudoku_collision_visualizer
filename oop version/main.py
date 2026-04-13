import flet as ft
from logic import Game


class NumberDraggable(ft.Draggable):
    def __init__(self, number, game, on_change_callback):
        self.number = number
        self.game = game
        self.on_change = on_change_callback

        draggable_container = ft.Container(
            width=50,
            height=50,
            bgcolor=ft.Colors.BLUE_GREY_800,
            border_radius=5,
            alignment=ft.alignment.center,
            content=ft.Text(str(self.number), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            # THE MAGIC TRIGGER: When clicked, run our new method
            on_click=self.highlight_board
        )

        feedback_container = ft.Container(
            width=50,
            height=50,
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY_800),
            border_radius=5,
            alignment=ft.alignment.center,
            content=ft.Text(str(self.number), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        )

        super().__init__(
            group="sudoku",
            content=draggable_container,
            content_feedback=feedback_container
        )

    def highlight_board(self, e):
        self.game.clear_highlights()

        self.game.fill_binary_highlight_array(self.number)

        self.on_change()


class BoardCell(ft.DragTarget):
    def __init__(self, row, column, board, on_change_callback):
        self.row = row
        self.column = column
        self.board = board
        self.on_change = on_change_callback

        self.text_element = ft.Text("", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)

        top_width = 3 if row % 3 == 0 else 1
        left_width = 3 if column % 3 == 0 else 1

        bottom_width = 3 if row == 8 else 0
        right_width = 3 if column == 8 else 0

        self.default_border = ft.border.only(
            top=ft.border.BorderSide(top_width, ft.Colors.BLACK),
            left=ft.border.BorderSide(left_width, ft.Colors.BLACK),
            bottom=ft.border.BorderSide(bottom_width, ft.Colors.BLACK),
            right=ft.border.BorderSide(right_width, ft.Colors.BLACK),
        )

        self.target_container = ft.Container(
            width=50,
            height=50,
            bgcolor=ft.Colors.GREY_300,
            border=self.default_border,  # Apply the smart border here
            alignment=ft.alignment.center,
            content=self.text_element
        )

        super().__init__(
            group="sudoku",
            content=self.target_container,
            on_accept=self.drag_accept,
            on_will_accept=self.drag_will_accept,
            on_leave=self.drag_leave
        )
        self.load_cell()

    def drag_will_accept(self, e):
        self.target_container.bgcolor = ft.Colors.YELLOW_200
        self.target_container.border = ft.border.all(3, ft.Colors.BLUE_ACCENT_400)
        self.update()

    def drag_leave(self, e):
        self.target_container.bgcolor = ft.Colors.GREY_300
        self.target_container.border = ft.border.all(1, ft.Colors.BLACK54)
        self.update()

    def drag_accept(self, e):
        src_object = e.page.get_control(e.src_id)
        dropped_number = src_object.number
        self.board.clear_highlights()
        self.board.fill_binary_highlight_array(dropped_number)

        if self.board.check_move(self.row, self.column):
            self.text_element.value = str(dropped_number)
            self.board.set_cell(self.row, self.column, dropped_number)

            self.target_container.bgcolor = ft.Colors.GREY_300
            self.target_container.border = ft.border.all(1, ft.Colors.BLACK54)
            self.update()

        self.on_change()


    def load_cell(self):
        cell_value = self.board.get_cell(self.row, self.column)

        if cell_value != 0:
            self.text_element.value = str(cell_value)
        else:
            self.text_element.value = ""

    def refresh_color(self):
        is_highlighted = self.board.bin_highlight_map[self.row][self.column]

        if is_highlighted == 1:
            self.target_container.bgcolor = ft.Colors.RED_200
        else:
            self.target_container.bgcolor = ft.Colors.GREY_300

        self.update()


def main(page: ft.Page):
    page.title = "Sudoku Collision Visualizer (O(1) Validation)"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 10
    page.theme_mode = ft.ThemeMode.DARK

    game = Game()
    game.fill_block_arr()
    game.load_puzzle()

    all_ui_cells = []

    def update_entire_board():
        for cell in all_ui_cells:
            cell.refresh_color()

    # 9x9 sudoku board
    board_layout = ft.Column(spacing=2)
    for row in range(9):
        row_items = []
        for col in range(9):
            new_cell = BoardCell(row, col, game, update_entire_board)
            row_items.append(new_cell)
            all_ui_cells.append(new_cell)
        board_layout.controls.append(
           ft.Row(controls=row_items, spacing=2, alignment=ft.MainAxisAlignment.CENTER)
          )

    # 1x9 number bank at the bottom
    bank_layout = ft.Row(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
    for i in range(1, 10):
        bank_layout.controls.append(NumberDraggable(i, game, update_entire_board))

    page.add(
        board_layout,
        ft.Divider(height=40, color=ft.Colors.TRANSPARENT),
        bank_layout
    )


if __name__ == "__main__":
    ft.app(target=main)