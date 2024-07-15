def get_corrected_mouse_position(mouse_x, mouse_y, screen_width, screen_height, scaled_width, scaled_height):
    pos = (mouse_x,mouse_y)
    # take the mouse position and scale it, too
    ratio_x = (screen_width / scaled_width)
    ratio_y = (screen_height / scaled_height)
    scaled_pos = (pos[0] / ratio_x, pos[1] / ratio_y)

    return scaled_pos

# Example usage
screen_width = 1280
screen_height = 720
scaled_width = 960
scaled_height = 720

mouse_positions = [
    (1256, 16),
    (1260, 12),
    (1272, 0),
    # Add more mouse positions if needed
]

for mouse_x, mouse_y in mouse_positions:
    corrected_x, corrected_y = get_corrected_mouse_position(mouse_x, mouse_y, screen_width, screen_height, scaled_width, scaled_height)
    print(f"Mouse Position: ({mouse_x}, {mouse_y}), Corrected Mouse Position: ({corrected_x}, {corrected_y})")
