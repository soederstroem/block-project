import pygame
from components.entity import Entity
from components.map import Tile

gravity = 0.3

def handle_collision(src: Entity, tgt: Tile):
    if not tgt.collidable:
        return

    src_rect = src.rect
    tgt_rect = tgt.rect

    # compute overlap amounts (positive values when intersecting)
    overlap_x = min(src_rect.right, tgt_rect.right) - max(src_rect.left, tgt_rect.left)
    overlap_y = min(src_rect.bottom, tgt_rect.bottom) - max(src_rect.top, tgt_rect.top)

    # approximate previous rect using velocity (player code updates pos before checks)
    prev_rect = src_rect.move(-int(src.velocity.x), -int(src.velocity.y))

    resolved = None
    # Swept checks: did we cross target boundary this frame?
    if prev_rect.right <= tgt_rect.left and src_rect.right > tgt_rect.left:
        resolved = "left"
    elif prev_rect.left >= tgt_rect.right and src_rect.left < tgt_rect.right:
        resolved = "right"
    elif prev_rect.bottom <= tgt_rect.top and src_rect.bottom > tgt_rect.top:
        resolved = "top"
    elif prev_rect.top >= tgt_rect.bottom and src_rect.top < tgt_rect.bottom:
        resolved = "bottom"

    # If ambiguous (corner) or no swept direction, resolve by smaller penetration
    if not resolved:
        if overlap_x < overlap_y:
            resolved = "left" if src_rect.centerx < tgt_rect.centerx else "right"
        else:
            resolved = "top" if src_rect.centery < tgt_rect.centery else "bottom"

    # Apply resolution and zero velocity on that axis
    if resolved == "left":
        src.pos.x = tgt_rect.left - src_rect.width
        src.velocity.x = 0
    elif resolved == "right":
        src.pos.x = tgt_rect.right
        src.velocity.x = 0
    elif resolved == "top":
        src.pos.y = tgt_rect.top - src_rect.height
        src.velocity.y = 0
        src.state = "standing"
    elif resolved == "bottom":
        src.pos.y = tgt_rect.bottom
        src.velocity.y = 0

    # keep rect in sync with pos
    src.rect.topleft = src.pos


def check_collision(src: Entity, tgt: Tile):
    if not tgt or not tgt.collidable:
        return False

    if not src.rect.colliderect(tgt.rect):
        return False

    prev_rect = src.rect.move(-int(src.velocity.x), -int(src.velocity.y))

    left_cross = prev_rect.right <= tgt.rect.left and src.rect.right > tgt.rect.left
    right_cross = prev_rect.left >= tgt.rect.right and src.rect.left < tgt.rect.right
    top_cross = prev_rect.bottom <= tgt.rect.top and src.rect.bottom > tgt.rect.top
    bottom_cross = prev_rect.top >= tgt.rect.bottom and src.rect.top < tgt.rect.bottom

    overlap_x = min(src.rect.right, tgt.rect.right) - max(src.rect.left, tgt.rect.left)
    overlap_y = min(src.rect.bottom, tgt.rect.bottom) - max(src.rect.top, tgt.rect.top)

    # Prefer clear swept direction when available
    if left_cross and not (top_cross or bottom_cross):
        return "left"
    if right_cross and not (top_cross or bottom_cross):
        return "right"
    if top_cross and not (left_cross or right_cross):
        return "top"
    if bottom_cross and not (left_cross or right_cross):
        return "bottom"

    # Ambiguous or simultaneous crossing (corner): resolve by smaller penetration
    if overlap_x < overlap_y:
        return "left" if src.rect.centerx < tgt.rect.centerx else "right"
    else:
        return "top" if src.rect.centery < tgt.rect.centery else "bottom"
    