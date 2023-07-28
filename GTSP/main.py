import pygame
import math
from class_library import Graph, Vertex

# method that turns off other buttons if one is clicked
def turnOffButtons(b1, b2, b3, b4):
    if b1:
        b1 = False
    if b2:
        b2 = False
    if b3:
        b3 = False
    if b4:
        b4 = False
    return b1, b2, b3, b4

# method that checks for collision between a rect and a mouse position
def checkCollision(rect, pos):
    if rect.pos.collidepoint(pos[0], pos[1]):
        return True
    else:
        return False
        

if __name__ == "__main__":
    
    # initialization
    pygame.init()
    w, h = 1280, 720
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    running = True
    G = Graph()

    # booleans for buttons
    place_vertex = False
    place_edge = False
    switch = True  # t/f switch for subsequent clicks
    delete_vertex = False
    delete_edge = False
    display_degree = False
    color_button = False

    # containers for holding mouse locations for drawing edges
    prev_pos = None
    current_pos = None

    # create button fonts
    font = pygame.font.SysFont('Corbel', 25)
    place_vertex_text = font.render("Place Vertex", True, "red")
    place_edge_text = font.render("Place Edge", True, "red")
    delete_vertex_text = font.render("Delete Vertex", True, "red")
    delete_edge_text = font.render("Delete Edge", True, "red")
    display_degree_text = font.render("Degree", True, "red")
    is_bipartite_text = font.render("Bipartite", True, "red")
    is_not_bipartite_text = font.render("Not Bipartite", True, "red")
    change_color_text = font.render("Color", True, "red")


    # running while loop
    while running:

        ev = pygame.event.get()  # get all events
        # render buttons
        mouse = pygame.mouse.get_pos()

        # loop for keeping the window open
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                raise SystemExit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # placing and deleting vertexes and edges logic

                # place vertex
                if place_vertex and not (0 <= mouse[0] <= screen.get_width() and 0 <= mouse[1] <= 50):
                    flag = False
                    for vertex in G.verticies:
                        if checkCollision(vertex, pos):
                            flag = True
                    if not flag:
                        new_rect = pygame.draw.circle(screen, "blue", pos, 10)
                        G.add_vertex(new_rect)
                    place_vertex = not place_vertex

                # delete vertex
                if delete_vertex and not (0 <= mouse[0] <= screen.get_width() and 0 <= mouse[1] <= 50):
                    G.remove_vertex(pos)
                    delete_vertex = not delete_vertex

                # place edge
                if place_edge and not (0 <= mouse[0] <= screen.get_width() and 0 <= mouse[1] <= 50):
                    for vertex in G.verticies:
                        if switch and checkCollision(vertex, pos):
                            prev_pos = vertex.pos.center
                            switch = not switch
                            break
                        if not switch and checkCollision(vertex, pos):
                            current_pos = vertex.pos.center
                            if prev_pos == current_pos:
                                new_rect = pygame.draw.arc(screen, "red", [current_pos[0], current_pos[1], 30, 30], math.radians(0),  math.radians(360))
                            else:
                                new_rect = pygame.draw.aaline(screen, "red", prev_pos, current_pos)
                            G.add_edge(new_rect, prev_pos, current_pos)
                            switch = not switch
                            place_edge = not place_edge
                            break
                            
                # delete edge
                if delete_edge and not (0 <= mouse[0] <= screen.get_width() and 0 <= mouse[1] <= 50):
                    G.remove_edge(pos)
                    delete_edge = not delete_edge

                # cycle color
                if color_button and not (0 <= mouse[0] <= screen.get_width() and 0 <= mouse[1] <= 50):
                    G.cycle_color(pos)


                # menu buttons logic

                # place vertex button
                if 30 <= mouse[0] <= 160 and 20 <= mouse[1] <= 50:
                    place_vertex = not place_vertex
                    place_edge, delete_vertex, delete_edge, color_button = turnOffButtons(place_edge, delete_vertex, delete_edge, color_button)

                # delete vertex button
                if 160 <= mouse[0] <= 290 and 20 <= mouse[1] <= 50:
                    delete_vertex = not delete_vertex
                    place_vertex, place_edge, delete_edge, color_button = turnOffButtons(place_vertex, place_edge, delete_edge, color_button)
                    
                # place edge button
                if 290 <= mouse[0] <= 420 and 20 <= mouse[1] <= 50:
                    place_edge = not place_edge
                    switch = True
                    place_vertex, delete_vertex, delete_edge, color_button = turnOffButtons(place_vertex, delete_vertex, delete_edge, color_button)

                # delete edge button
                if 420 <= mouse[0] <= 550 and 20 <= mouse[1] <= 50:
                    delete_edge = not delete_edge
                    place_vertex, delete_vertex, place_edge, color_button = turnOffButtons(place_vertex, delete_vertex, place_edge, color_button)

                # display degree button
                if 550 <= mouse[0] <= 620 and 20 <= mouse[1] <= 50:
                    display_degree = not display_degree

                # change color button
                if 630 <= mouse[0] <= 700 and 20 <= mouse[1] <= 50:
                    color_button = not color_button
                    place_vertex, delete_vertex, place_edge, delete_edge = turnOffButtons(place_vertex, delete_vertex, place_edge, delete_edge)
            
            
        # Render the graphics here

        # paint screen black
        screen.fill("black")

        # render place vertex button
        if 30 <= mouse[0] <= 160 and 20 <= mouse[1] <= 50 or place_vertex == True:
            pygame.draw.rect(screen, "grey", [30,20,125,25])
        else:
            pygame.draw.rect(screen, "black", [30,20,125,25])
        screen.blit(place_vertex_text, [30,20,50,50])

        # render delete vertex button
        if 160 <= mouse[0] <= 290 and 20 <= mouse[1] <= 50 or delete_vertex == True:
            pygame.draw.rect(screen, "grey", [160,20,135,25])
        else:
            pygame.draw.rect(screen, "black", [160,20,135,25])
        screen.blit(delete_vertex_text, [160,20,135,25])

        # render place edge button
        if 290 <= mouse[0] <= 420 and 20 <= mouse[1] <= 50 or place_edge == True:
            pygame.draw.rect(screen, "grey", [300,20,115,25])
        else:
            pygame.draw.rect(screen, "black", [300,20,115,25])
        screen.blit(place_edge_text, [300,20,115,25])

        # render delete edge button
        if 420 <= mouse[0] <= 550 and 20 <= mouse[1] <= 50 or delete_edge == True:
            pygame.draw.rect(screen, "grey", [420,20,125,25])
        else:
            pygame.draw.rect(screen, "black", [420,20,125,25])
        screen.blit(delete_edge_text, [420,20,125,50])

        # render display degree button
        if 550 <= mouse[0] <= 620 and 20 <= mouse[1] <= 50 or display_degree == True:
            pygame.draw.rect(screen, "grey", [550,20,75,25])
        else:
            pygame.draw.rect(screen, "black", [550,20,75,25])
        screen.blit(display_degree_text, [550,20,75,50])

        # render color button
        if 630 <= mouse[0] <= 700 and 20 <= mouse[1] <= 50 or color_button == True:
            pygame.draw.rect(screen, "grey", [630,20,60,25])
        else:
            pygame.draw.rect(screen, "black", [630,20,60,25])
        screen.blit(change_color_text, [630,20,50,50])

        # render is bipartite signal
        if G.bipartite:
            screen.blit(is_bipartite_text, [700,20,150,50])
        else:
            screen.blit(is_not_bipartite_text, [700,20,150,50])


        # display degrees of vertices
        if display_degree:
            for vertex in G.verticies:
                screen.blit(font.render("{}".format(vertex.degree), True, "light blue"), [vertex.pos[0]-20, vertex.pos[1]-20, vertex.pos[2]-20, vertex.pos[3]-20])

        # render text
        n_count_text = font.render("{}".format(G.n), True, "red")
        m_count_text = font.render("{}".format(G.m), True, "red")
        k_count_text = font.render("{}".format(G.k), True, "red")

        # render n counter
        screen.blit(n_count_text, [1000, 20, 125, 50])

        # render m counter
        screen.blit(m_count_text, [1050, 20, 125, 50])

        # render k counter
        screen.blit(k_count_text, [1100, 20, 125, 50])        


        # keep edges drawn
        for edge in G.edges:
            if edge.start == edge.end:
                pygame.draw.arc(screen, "red", [edge.start[0], edge.end[1], 30, 30], math.radians(0),  math.radians(360)) # TODO fix loops drawing
            else:
                pygame.draw.aaline(screen, "red", edge.start, edge.end)

        # keep vertexes drawn
        for vertex in G.verticies:
            pygame.draw.circle(screen, vertex.colors[vertex.display_color], (vertex.__getitem__(0)+10, vertex.__getitem__(1)+10), 10)

        
        # update window
        G.update_graph()       # update graph info after each event
        pygame.display.flip()  # refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 fps)


