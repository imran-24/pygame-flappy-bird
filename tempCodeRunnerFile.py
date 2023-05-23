self.all_sprite.update(dt)
            
            self.collision_sprite.draw(self.display_surface)
            self.score = self.show_score()
            self.coll