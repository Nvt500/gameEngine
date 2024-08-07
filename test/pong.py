import engine
import random
from time import sleep


def pick_mode() -> bool | None:
       
    choice1_text = engine.Text(text="Player vs CPU", position=engine.Vector2(1, 3))
    choice2_text = engine.Text(text="Player vs Player", position=engine.Vector2(1, 6))
    
    choice_screen = engine.Screen(size=engine.Vector2(18, 9), background={"icon": " "})
    
    choice_screen.add_objects(0, choice1_text, choice2_text)
    
    choice1 = True
    while True:
        
        if choice1:
            choice1_text.blink(10)
        else:
            choice2_text.blink(10)
        
        if choice_screen.get_key(engine.Keys.W):
            choice1 = True
        if choice_screen.get_key(engine.Keys.S):
            choice1 = False
        if choice_screen.get_key(engine.Keys.ENTER) or choice_screen.get_key(engine.Keys.SPACE):
            return choice1
        
        choice_screen.update()
        
        if choice_screen.get_key(engine.Keys.Q):
            choice_screen.close()
            return None
    
    choice_screen.close()


def main() -> None:
    
    if (player_vs_cpu := pick_mode()) is None:
        return
        
    player = engine.Rect(size=engine.Vector2(1, 3), position=engine.Vector2(1, 6))
    
    paddle = engine.Rect(size=engine.Vector2(1, 3), position=engine.Vector2(19, 6))#, update_every_x_frames=3)
    
    ball = engine.Rect(size=engine.Vector2.ONE, position=engine.Vector2(10, 7), update_every_x_frames=3)
    
    score = engine.Text(text="0|0", position=engine.Vector2(9, 1))
    
    screen = engine.Screen(size=engine.Vector2(21, 15), background={"icon": " "})
    
    screen.add_objects(0, player, ball, paddle, score)
        
    ball_velocities = [engine.Vector2.UPRIGHT, engine.Vector2.DOWNRIGHT, engine.Vector2.UPLEFT, engine.Vector2.DOWNLEFT]
    ball_velocity = random.choice(ball_velocities)
    
    if player_vs_cpu:
        paddle.change_update_every_x_frames(3)
    
    sleep(0.5)
    
    while not screen.get_key(engine.Keys.Q):
        
        if screen.get_key(engine.Keys.W):
            player.change_position(engine.Vector2.UP)
        if screen.get_key(engine.Keys.S):
            player.change_position(engine.Vector2.DOWN)
        
        
        if ball.position.y == 0 or ball.position.y == screen.BOTTOM:
            ball_velocity.y *= -1
        if ball.check_if_inside_rect(player) or ball.check_if_inside_rect(paddle):
            ball_velocity.x *= -1
        
        if player_vs_cpu:
            if ball.position.y - (paddle.position.y - 1) < 0:
                paddle.change_position(engine.Vector2.UP)
            if ball.position.y - (paddle.position.y - 1) > 0:
                paddle.change_position(engine.Vector2.DOWN)
        else:
            if screen.get_key(engine.Keys.UP):
                paddle.change_position(engine.Vector2.UP)
            if screen.get_key(engine.Keys.DOWN):
                paddle.change_position(engine.Vector2.DOWN)
        
        ball.change_position(ball_velocity)
        
        screen.update()
            
        if ball.position.x == screen.LEFT:
            score.change_text(f"{score.text[0]}|{int(score.text[2]) + 1}")
            ball_velocity = random.choice(ball_velocities[2:])
            ball.position = engine.Vector2(10, 7)
            player.position.y = 6
            paddle.position.y = 6
            screen.update()
            sleep(1)
        if ball.position.x == screen.RIGHT:
            score.change_text(f"{int(score.text[0]) + 1}|{score.text[2]}")
            ball_velocity = random.choice(ball_velocities[:2])
            ball.position = engine.Vector2(10, 7)
            player.position.y = 6
            paddle.position.y = 6
            screen.update()
            sleep(1)
    
    screen.close()


if __name__ == "__main__":
    main()