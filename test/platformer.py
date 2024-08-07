import engine
from time import sleep


def main() -> None:
    
    try:
        debug = engine.Debug()
        text = engine.Text(text="HELLO", position=engine.Vector2(10, 2), name="hello_text")
        
        player = engine.Rect(size=engine.Vector2(1, 1), position=engine.Vector2(2, 6), name="player", gravity={"update_every_x_frames": 5}, static=False)
        box = engine.Rect(size=engine.Vector2(2, 2), position=engine.Vector2(10, 13), sprite={"icon": "/"}, name="box", gravity={"update_every_x_frames": 5}, static=False)
        
        ground = engine.Rect(size=engine.Vector2(40, 1), position=engine.Vector2(0, 15), sprite={"icon": "~"}, name="ground")
        tower = engine.Rect(size=engine.Vector2(3,8), position=engine.Vector2(17, 7), sprite={"icon": "+-+"})
        tower2 = engine.Rect(size=engine.Vector2(3,8), position=engine.Vector2(25, 7), sprite={"icon": "+-+"})
        
        path = engine.Path(engine.Vector2(14, 15), engine.Vector2(6, 7),  engine.Vector2(14, 7))
        moving_platform = engine.Rect(size=engine.Vector2(3, 1), position=path.start, sprite={"icon": "="}, update_every_x_frames=10, path=path, sticky=True)
        
        path2 = engine.Path(engine.Vector2(25, 7), engine.Vector2(17, 7))
        moving_platform2 = engine.Rect(size = engine.Vector2(3, 1), position=path2.start, sprite={"icon": "="}, update_every_x_frames=10, path=path2, sticky=True)
                
        movables_cl = engine.CollisionLayer(name="player", objects=[player, box], collide_with_self=True)
        obstacles_cl = engine.CollisionLayer(name="obstacles", objects=[moving_platform, moving_platform2, ground, tower, tower2])
        
        movables_cl.create_masks(obstacles_cl)
        
        goal = engine.Rect(size=engine.Vector2(2, 2), position=engine.Vector2(38, 13), sprite={"icon": "\\//\\"})
        
        screen = engine.DynamicScreen(size=engine.Vector2(20, 16), center=player, offset=engine.Vector2(0, 7), get_input=True, background={"icon": " "})
        screen.init()
        
        screen.add_objects(0, movables_cl, obstacles_cl, goal, debug, text)
        
        win = False
        player_velocity = engine.Vector2.ZERO
        moving_platform_velocity = engine.Vector2.UP
        while not screen.get_key(engine.Keys.Q):
            
            player_velocity.x = 0
            if player_velocity.y == 0 and screen.get_key(engine.Keys.W) and player.is_on_floor:
                player_velocity.y -= 2
            if screen.get_key(engine.Keys.D):
                player_velocity.x += 1
            if screen.get_key(engine.Keys.A):
                player_velocity.x -= 1
            
            player.change_position(engine.Vector2(player_velocity.x, player_velocity.y))
            
            if player_velocity.y < 0 :
                player_velocity.y += 1
            
            if box.check_if_inside_rect(goal):
                win = True
                break
                        
            debug.print(player.position)
                        
            screen.update()
        screen.close()
        
        sleep(0.1)
        
        if win:
            text = engine.Text(text="You Win!", position=engine.Vector2(1, 4), name="win_text")

            screen = engine.Screen(size=engine.Vector2(10, 9), get_input=True)
            screen.init()

            screen.add_objects(0, text)

            while not screen.get_key(engine.Keys.Q):
                screen.update()
                
            screen.close()
        
    except Exception as e:
        screen.close()
        print(e)
    

if __name__ == "__main__":
    main()