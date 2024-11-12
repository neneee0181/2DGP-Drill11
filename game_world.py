world = [[] for _ in range(4)]
collision_pairs = {}


def add_object(o, depth=0):
    world[depth].append(o)


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]  # 비어져있으면 빈 값으로 초기화
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def add_objects(ol, depth=0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)  # world에서 o를 삭제.
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()


# fill here
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def handle_collisions():
    # 게임 월드에 등록된 충돌 정보를 바탕으로, 실제 충돌 검사를 수행.
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:  # a 리스트에서 하나 뽑고,
            for b in pairs[1]:  # b 리스트에서 하나 뽑고,
                if collide(a, b):
                    print(f'{group} collide')
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
