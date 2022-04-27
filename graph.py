from random import choice

subjects = {
    "something wrong\nwith the world": ["bagels", "the weather"],
    "bagels": ["New York!", "buses"],
    "New York!": ["guns", "getting mugged", "the weather"],
    "guns": ["getting mugged", "buses", "cuckoo clocks!"],
    "getting mugged": ["New York!"],
    "the weather": ["the office door", "a meeting on\nthe stairs"],
    "the office door": ["architects"],
    "a meeting on\nthe stairs": ["architects"],
    "architects": ["emails", "a teams meeting", "OOP", "something wrong\nwith the world"],
    "buses": ["transport planning", "philosophy"],
    "cuckoo clocks!": ["a teams meeting", "transport planning", "something wrong\nwith the world"],
    "emails": ["transport planning", "a teams meeting"],
    "a teams meeting": ["transport planning", "cuckoo clocks!", "something wrong\nwith the world"],
    "OOP": ["anthropomorphism", "something wrong\nwith the world"],
    "transport planning": ["something wrong\nwith the world"],
    "philosophy": ["something wrong\nwith the world"],
    "anthropomorphism": ["the xmas instance"],
    "the xmas instance": ["philosophy"]
}

state_of_mind = {
    "carefully explain": ["reminisce about", "get iritated\nabout"],
    "reminisce about": ["fondly remember", "carefully explain"],
    "fondly remember": ["pivot wildly to", "get iritated\nabout"],
    "get iritated\nabout": ["exclaim angrily\nabout", "dryly elaborate\non"],
    "pivot wildly to": ["pivot wildly to", "exclaim angrily\nabout"],
    "exclaim angrily\nabout": ["carefully explain"],
    "dryly elaborate\non": ["pivot wildly to"]
}


class GraphTraverser:

    def __init__(self, graph, state=None):
        self.graph = graph

        # todo check graph

        if state == None:
            self.state = choice(list(graph.keys()))
        else:
            self.state = state
        if self.state not in self.graph:
            raise UserWarning(f"Cannot find vertex: {self.state} in graph.")

    def traverse(self):
        if self.state not in self.graph:
            raise UserWarning(f"You have reached a dead end at state {self.state}")
        self.state = choice(self.graph.get(self.state))
        return self.state