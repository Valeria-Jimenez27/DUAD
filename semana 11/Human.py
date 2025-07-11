class Head:
    def __init__(self, eyes, nose, mouth, ears):
        self.eyes = eyes
        self.nose = nose
        self.mouth = mouth
        self.ears = ears    

class Torso:
    def __init__(self, espine, heart, lungs, intestines, stomach, liver):
        self.espine = espine
        self.heart = heart
        self.lungs = lungs
        self.intestines = intestines
        self.stomach = stomach
        self.liver = liver

class Hand:
    def __init__(self, fingers, nails):
        self.fingers = fingers
        self.nails = nails

class Arm:
    def __init__(self, hand, elbow, shoulder):
        self.hand = hand
        self.elbow = elbow
        self.shoulder = shoulder

class Feet:
    def __init__(self, toes):
        self.toes = toes

class Leg:
    def __init__(self, feet, knee, heel):
        self.feet = feet
        self.knee = knee
        self.heel = heel

class Human:
    def __init__(self, head, torso, right_arm, right_leg, left_arm, left_leg):
        self.head = head
        self.torso = torso
        self.right_arm = right_arm
        self.right_leg = right_leg
        self.left_arm = left_arm
        self.left_leg = left_leg

head = Head(eyes=2, nose=1, mouth=1, ears=2)
torso = Torso(espine=1, heart=1, lungs=2, intestines=2, stomach=1, liver=1)

left_hand = Hand(fingers=5, nails=5)
right_hand = Hand(fingers=5, nails=5)

left_arm = Arm(hand=left_hand, shoulder=1, elbow=1)
right_arm = Arm(hand=right_hand, shoulder=1, elbow=1)

left_foot = Feet(toes=5)
right_foot = Feet(toes=5)

left_leg = Leg(feet=left_foot, knee=1, heel=1)
right_leg = Leg(feet=right_foot, knee=1, heel=1)

human = Human(head, torso, right_arm, right_leg, left_arm, left_leg)

