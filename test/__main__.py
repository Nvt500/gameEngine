import engine

def main() -> None:
    
    hello = engine.Text(text="0\n0", position=engine.Vector2(9, 0), name="hello")
        
    player = engine.Rect(size=engine.Vector2(1, 1), position=engine.Vector2(0,0), name="player")
    box = engine.Rect(size=engine.Vector2(4, 4), position=engine.Vector2(6, 6), sprite={"icon": "X"}, name="box")
    other_box = engine.Rect(size=engine.Vector2(1, 2), position=engine.Vector2(0, 8), sprite={"icon": "O"}, name="other_box")
    
    obstacles_cl = engine.CollisionLayer("obstacles", objects=[box, other_box])
    
    player_cl = engine.CollisionLayer("player", objects=[player])
    
    player_cl.create_masks(obstacles_cl)
    
    screen = engine.Screen(size=engine.Vector2(10, 10), get_input=True)
    screen.init()
    
                   
    screen.add_objects(0, player, box, other_box, hello)
    
    while not screen.get_key(engine.Keys.Q):
        
        velocity = engine.Vector2.ZERO
        
        if screen.get_key(engine.Keys.D):
            velocity.x += 1
        if screen.get_key(engine.Keys.A):
            velocity.x += -1
        if screen.get_key(engine.Keys.W):
            velocity.y += -1
        if screen.get_key(engine.Keys.S):
            velocity.y += 1
          
        if velocity != engine.Vector2.ZERO:
            player.change_position(velocity)
        
        hello.change_text(f"{player.position.x}\n{player.position.y}")
        
        screen.update()
    
    screen.close()
    

if __name__ == "__main__":
    main()