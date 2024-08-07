import engine
from math import floor

def main() -> None:
    
    try:
        score = engine.Text(text="0", position=engine.Vector2(9, 1), name="score")

        player = engine.Rect(size=engine.Vector2(1, 1), position=engine.Vector2(2, 6), name="player", gravity={"update_every_x_frames": 6})
        ground = engine.Rect(size=engine.Vector2(20, 1), position=engine.Vector2(0, 15), sprite={"icon": "^"}, name="ground")

        pipe1 = engine.Rect(size=engine.Vector2(2, 5), position=engine.Vector2(15, 0), name="pipe", update_every_x_frames=5)
        pipe2 = engine.Rect(size=engine.Vector2(2, 5), position=engine.Vector2(15, 10), name="pipe", update_every_x_frames=5)

        screen = engine.Screen(size=engine.Vector2(20, 16), get_input=True, background={"icon": " "})
        screen.init()

        screen.add_objects(0, player, ground, score, pipe1, pipe2)
        
        while not screen.get_key(engine.Keys.SPACE):
            screen.update()
        
        velocity = 0
        s = 0
        while not screen.get_key(engine.Keys.Q):

            if velocity == 0 and screen.get_key(engine.Keys.SPACE):
                velocity -= 1

            player.change_position(engine.Vector2(0, floor(velocity)))

            if velocity < 0 :
                velocity += 0.5
                
            if pipe1.position.x == 0:
                pipe1.set_position(engine.Vector2(screen.RIGHT - 1, 0))
                pipe2.set_position(engine.Vector2(screen.RIGHT - 1, 10))
                s += 1
                score.change_text(s)
            
            pipe1.change_position(engine.Vector2.LEFT)
            pipe2.change_position(engine.Vector2.LEFT)
            
            if player.check_collision_with_rect(pipe1) or player.check_collision_with_rect(pipe2) or player.check_collision_with_rect(ground):
                score.change_text(f"You Died\n{s}")
                while not screen.get_key(engine.Keys.SPACE):
                    screen.update()
                break
            
            screen.update()
        
        screen.close()
    except Exception as e:
        screen.close()
        print(e)
    

if __name__ == "__main__":
    main()