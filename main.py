from grid import Grid
# DPS means debug print statement

def player_move(grid, current_player, empty_cells):
    """
    Modify the grid based on player input.
    :param grid: Grid, the current game
    :param current_player: str, the player's character
    :param empty_cells: list, unoccupied cells as tuples
    """
    while True:
        if len(empty_cells) > 1:            # moves can still be made, auto-play not required
            try:
                row, col = map(int, input(f"Player {current_player}, where do you want to place your choice (row col)? e.g. 1 1: ").split())
                grid.modify_cell(current_player, row, col)
                break
            except ValueError:
                print("Invalid input. Please enter the row and column numbers separated by a space, e.g. 1 1.")
                print()
        else:  # auto-play
            row, col = empty_cells[0]
            grid.modify_cell(current_player, row, col)
            break

def game_play():
    play_again = "y"
    while play_again == "y":
        print("Do you want to play against a friend (F) or against the computer (C)?")
        mode = (input("Choose game mode: ")).upper()
        while mode not in ["F", "C"]:
            print("Invalid input.", end=" ")
            mode = (input("Choose game mode: F or C? ")).upper()
        print()

        n = 3       # grid size
        current_player = "X"
        grid = Grid(n)
        print(grid)

        game_over = False
        while not game_over:
            result, game_over = grid.status_check()
            if game_over:
                print(f"Game over! {result}")
                break

            empty_cells = grid.empty_cells()
            if mode == "F":
                player_move(grid, current_player, empty_cells)
            else:
                if current_player == "X":
                    player_move(grid, current_player, empty_cells)
                else:
                    print(f"Player {current_player} has played.")
                    grid.computer_move(current_player, "X")


            current_player = "X" if current_player == "O" else "O"          # alternate players

        print()
        play_again = (input("Do you want to play again? yes (y)/ no (n): ")).lower()
        print()

    print("Thanks for playing with us!")

def main():
    game_play()

if __name__ == '__main__':
    main()
