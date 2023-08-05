#!/usr/bin/env python

from __future__ import print_function, division, absolute_import

import random 
import re
import toytree


#######################################################
# Exception Classes
#######################################################
class ToytreeError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class TreeError(Exception):
    "A problem occurred during a TreeNode operation"
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return repr(self.value)

# TREE FORMATS
NW_FORMAT = {
    # flexible with support
    # Format 0 = (A:0.35,(B:0.72,(D:0.60,G:0.12)1.00:0.64)1.00:0.56);
    0: [
        ('name', str, True),
        ('dist', float, True),
        ('support', float, True),
        ('dist', float, True),
    ],

    # flexible with internal node names
    # Format 1 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E:0.64)C:0.56);
    1: [
        ('name', str, True),
        ('dist', float, True),
        ('name', str, True),
        ('dist', float, True),      
    ],

    # strict with support values
    # Format 2 = (A:0.35,(B:0.72,(D:0.60,G:0.12)1.00:0.64)1.00:0.56);
    2: [
        ('name', str, False),
        ('dist', float, False),
        ('support', str, False),
        ('dist', float, False),      
    ],

    # strict with internal node names
    # Format 3 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E:0.64)C:0.56);
    3: [
        ('name', str, False),
        ('dist', float, False),
        ('name', str, False),
        ('dist', float, False),      
    ],

    # strict with internal node names
    # Format 4 = (A:0.35,(B:0.72,(D:0.60,G:0.12)));
    4: [
        ('name', str, False),
        ('dist', float, False),
        (None, None, False),
        (None, None, False),      
    ],

    # Format 5 = (A:0.35,(B:0.72,(D:0.60,G:0.12):0.64):0.56);
    5: [
        ('name', str, False),
        ('dist', float, False),
        (None, None, False),
        ('dist', float, False),      
    ],

    # Format 6 = (A:0.35,(B:0.72,(D:0.60,G:0.12)E)C);
    6: [
        ('name', str, False),
        (None, None, False),
        (None, None, False),        
        ('dist', float, False),      
    ],

    # Format 7 = (A,(B,(D,G)E)C);
    7: [
        ('name', str, False),
        ('dist', float, False),
        ('name', str, False),        
        (None, None, False),        
    ],    


    # Format 8 = (A,(B,(D,G)));
    8: [
        ('name', str, False),
        (None, None, False),
        ('name', str, False),        
        (None, None, False),
    ],

    # Format 9 = (,(,(,)));
    9: [
        ('name', str, False),
        (None, None, False),
        (None, None, False),
        (None, None, False),
    ],    

    # Format 10 = ((a[&Z=1,Y=2]:1.0[&X=3], b[&Z=1,Y=2]:3.0[&X=2]):1.0[&L=1,W=0], ...
    # NHX Like mrbayes NEXUS common
    10: [
        ('name', str, True),
        ('dist', str, True),
        ('name', str, True),
        ('dist', str, True),
    ]
}



#######################################################
# Branch modification Class
#######################################################
class TreeMod:
    """
    Return a tree with edge lengths modified according to one of 
    the mod functions. 
    """
    def __init__(self, ttree):
        self._ttree = ttree

    def node_scale_root_height(self, treeheight=1):
        """
        Returns a toytree copy with all nodes multiplied by a constant so that
        the root height equals the value entered for treeheight.
        """
        # make tree height = 1 * treeheight
        ctree = self._ttree.copy()
        _height = ctree.treenode.height
        for node in ctree.treenode.traverse():
            node.dist = (node.dist / _height) * treeheight
        ctree._coords.update()
        return ctree


    def node_slider(self, prop=0.999, seed=None):
        """
        Returns a toytree copy with node heights modified while retaining 
        the same topology but not necessarily node branching order. 
        Node heights are moved up or down uniformly between their parent 
        and highest child node heights in 'levelorder' from root to tips.
        The total tree height is retained at 1.0, only relative edge
        lengths change.
        """
        # I don't think users should need to access prop
        prop = prop
        assert isinstance(prop, float), "prop must be a float"
        assert prop < 1, "prop must be a proportion >0 and < 1."
        random.seed(seed)

        # make copy and iter nodes from root to tips
        ctree = self._ttree.copy()
        for node in ctree.treenode.traverse():

            # slide internal nodes 
            if node.up and node.children:

                # get min and max slides
                # minjit = max([i.dist for i in node.children]) * prop
                # maxjit = (node.up.height * prop) - node.height

                # the closest child to me
                minchild = min([i.dist for i in node.children])

                # prop distance down toward child
                minjit = minchild * prop

                # prop towards parent
                maxjit = node.dist * prop

                # node.height
                newheight = random.uniform(
                    node.height - minjit, node.height + maxjit)

                # how much lower am i?
                delta = newheight - node.height

                # edges from children to reach me
                for child in node.children:
                    child.dist += delta

                # slide self to match
                node.dist -= delta

        # update new coords
        ctree._coords.update()
        return ctree


    def node_multiplier(self, multiplier=0.5, seed=None):
        """
        Returns a toytree copy with all nodes multiplied by a constant 
        sampled uniformly between (multiplier, 1/multiplier).
        """
        random.seed(seed)
        ctree = self._ttree.copy()
        low, high = sorted([multiplier, 1. / multiplier])
        mult = random.uniform(low, high)
        for node in ctree.treenode.traverse():
            node.dist = node.dist * mult
        ctree._coords.update()
        return ctree


    def make_ultrametric(self, strategy=1):
        """
        Returns a tree with branch lengths transformed so that the tree is 
        ultrametric. Strategies include:
        (1) tip-align: 
            extend tips to the length of the fartest tip from the root; 
        (2) NPRS: 
            non-parametric rate-smoothing: minimize ancestor-descendant local 
            rates on branches to align tips (not yet supported); and 
        (3) penalized-likelihood: 
            not yet supported.
        """
        ctree = self._ttree.copy()

        if strategy == 1:
            for node in ctree.treenode.traverse():
                if node.is_leaf():
                    node.dist += node.height
                    # node.dist = node.height + 1

        else:
            raise NotImplementedError(
                "Strategy {} not yet implemented. Seeking developers."
                .format(strategy))

        return ctree







# class TreeInference:
# - get distance matrix (from an input data set... phy, nex)
# - ----- create a class to store DNA matrix (pandas colored)
# - NJ tree infer
#   ------ uses distance matrix
# - UPGMA tree infer
#   ------ uses distance matrix


#class TreeMoves:
#     def move_spr(self):
#         """
#         Sub-tree pruning and Regrafting. 
#         Select one edge randomly from the tree and split on that edge to create
#         two subtrees. Attach one of the subtrees (e.g., the smaller one) 
#         randomly to the larger tree to create a new node.
#         ... does SPR break edges connected to root when tree is real rooted?
#         """
#         pass
#         # On rooted trees we can work with nodes easier than edges. Start by
#         # selected a node at random that is not root.
#         # nodes = [i for i in self.ttree.tree.traverse() if not i.is_root()]
#         # rnode = nodes[random.randint(0, len(nodes) - 1)]
#         # # get all edges on the tree, skip last one which is non-real root edge
#         # edges = self.ttree.tree.get_edges()[:-1]
#         # # select a random edge
#         # redge = edges[random.randint(0, len(edges))]
#         # # break into subtrees
#         # tre1 = self.tree.prune(self.tree.get_common_ancestor(redge[0]).idx)
#         # tre2 = self.tree.prune(self.tree.get_common_ancestor(redge[1]).idx)



#     def move_tbr(self):
#         pass


#     def move_nni(self):
#         pass


#     def non_parametric_rate_smoothing(self):
#         """
#         Non-parametric rate smooting.
#         A method for estimating divergence times when evolutionary rates are 
#         variable across lineages by minimizing ancestor-descendant local rate
#         changes. According to Sanderson this method is motivated by the 
#         likelihood that evolutionary rates are autocorrelated in time.

#         returns Toytree
#         """
#         # p is a fixed exponent
#         p = 2
#         W = []
#         for node in self.ttree.traverse():
#             if not node.is_leaf():
#                 children = node.children
#                 ks = []
#                 for child in children:
#                     dist = abs(node.dist - child.dist)
#                     ks.append(dist ** p)
#                 W.append(sum(ks))

#         # root rate is mean of all descendant rates -- 
#         # n is the number of edges (rates) (nnodes - 1 for root)
#         r_root = np.mean(W)
#         rootw = []
#         for child in self.ttree.tree.children:
#             rootw.append((r_rroot - child.dist) ** p)
#         w_root = sum(rootw)
#         W.append(w_root)
#         k = []
#         for 
#         k = sum(  np.exp(abs(ri - rj), p)  )
#         W = sum(k)


#     def penalized_likelihood(...):
#         pass
#

# def wfunc(ttree, p):
#     ws = []
#     for node in ttree.tree.traverse():
#         if not node.is_leaf():          
#             w = sum([(node.dist - child.dist) ** p for child in node.children])
#             ws.append(w)
#     return sum(ws)





#######################################################
# Random Tree generation Class
#######################################################
class RandomTree(object):

    @staticmethod
    def coaltree(ntips, ne=None, seed=None):
        """
        Returns a coalescent tree with ntips samples and waiting times 
        between coalescent events drawn from the kingman coalescent:
        (4N)/(k*(k-1)), where N is population size and k is sample size.
        Edge lengths on the tree are in generations.

        If no Ne argument is entered then edge lengths are returned in units
        of 2*Ne, i.e., coalescent time units. 
        """
        # seed generator
        random.seed(seed)

        # convert units
        coalunits = False
        if not ne:
            coalunits = True
            ne = 10000

        # build tree: generate N tips as separate Nodes then attach together 
        # at internal nodes drawn randomly from coalescent waiting times.
        tips = [
            toytree.tree().treenode.add_child(name=str(i)) 
            for i in range(ntips)
        ]
        while len(tips) > 1:
            rtree = toytree.tree()
            tip1 = tips.pop(random.choice(range(len(tips))))
            tip2 = tips.pop(random.choice(range(len(tips))))
            kingman = (4. * ne) / float(ntips * (ntips - 1))
            dist = random.expovariate(1. / kingman)
            rtree.treenode.add_child(tip1, dist=tip2.height + dist)
            rtree.treenode.add_child(tip2, dist=tip1.height + dist)
            tips.append(rtree.treenode)

        # build new tree from the newick string
        self = toytree.tree(tips[0].write())    
        self.treenode.ladderize()

        # make tree edges in units of 2N (then N doesn't matter!)
        if coalunits:
            for node in self.treenode.traverse():
                node.dist /= (2. * ne)

        # ensure tips are at zero (they sometime vary just slightly)
        for node in self.treenode.traverse():
            if node.is_leaf():
                node.dist += node.height

        # set tipnames
        for tip in self.get_tip_labels():
            node = self.treenode.search_nodes(name=tip)[0]
            node.name = "r{}".format(node.idx)

        # decompose fills in internal node names and idx
        self._coords.update()
        return self


    @staticmethod
    def unittree(ntips, treeheight=1.0, seed=None):
        """
        Returns a random tree topology w/ N tips and a root height set to
        1 or a user-entered treeheight value. Descendant nodes are evenly 
        spaced between the root and time 0.

        Parameters
        -----------
        ntips (int):
            The number of tips in the randomly generated tree

        treeheight(float):
            Scale tree height (all edges) so that root is at this height.

        seed (int):
            Random number generator seed.
        """
        # seed generator
        random.seed(seed)

        # generate tree with N tips.
        tmptree = toytree.tree().treenode  # TreeNode()
        tmptree.populate(ntips)
        self = toytree.tree(newick=tmptree.write())

        # set tip names by labeling sequentially from 0
        self = (
            self
            .ladderize()
            .mod.make_ultrametric()
            .mod.node_scale_root_height(treeheight)
        )

        # set tipnames randomly (doesn't have to match idx)
        nidx = list(range(self.ntips))
        random.shuffle(nidx)
        for tidx, node in enumerate(self.treenode.get_leaves()):
            node.name = "r{}".format(nidx[tidx])

        for node in self.treenode.traverse():
            node.support = 100            
        # fill internal node names and idx
        self.treenode.ladderize()
        self._coords.update()
        return self


    @staticmethod
    def imbtree(ntips, treeheight=1.0):
        """
        Return an imbalanced (comb-like) tree topology.
        """
        rtree = toytree.tree()
        rtree.treenode.add_child(name="r0")
        rtree.treenode.add_child(name="r1")

        for i in range(2, ntips):
            # empty node
            cherry = toytree.tree()
            # add new child
            cherry.treenode.add_child(name="r" + str(i))
            # add old tree
            cherry.treenode.add_child(rtree.treenode)
            # update rtree
            rtree = cherry

        # get toytree from newick            
        tre = toytree.tree(rtree.write(tree_format=9))
        tre = tre.mod.make_ultrametric()
        self = tre.mod.node_scale_root_height(treeheight)
        self._coords.update()
        return self


    @staticmethod
    def baltree(ntips, treeheight=1.0):
        """
        Returns a balanced tree topology.
        """
        # require even number of tips
        if ntips % 2:
            raise ToytreeError("balanced trees must have even number of tips.")

        # make first cherry
        rtree = toytree.tree()
        rtree.treenode.add_child(name="r0")
        rtree.treenode.add_child(name="r1")

        # add tips in a balanced way
        for i in range(2, ntips):

            # get node to split
            node = return_small_clade(rtree.treenode)

            # add two children
            node.add_child(name=node.name)
            node.add_child(name="r" + str(i))

            # rename ancestral node
            node.name = None

        # rename tips so names are in order
        idx = len(rtree) - 1
        for node in rtree.treenode.traverse("postorder"):
            if node.is_leaf():
                node.name = "r" + str(idx)
                idx -= 1

        # get toytree from newick            
        tre = toytree.tree(rtree.write(tree_format=9))
        tre = tre.mod.make_ultrametric()
        self = tre.mod.node_scale_root_height(treeheight)
        self._coords.update()
        return self        



#######################################################
# Other
#######################################################
def bpp2newick(bppnewick):
    "converts bpp newick format to normal newick"
    regex1 = re.compile(r" #[-+]?[0-9]*\.?[0-9]*[:]")
    regex2 = re.compile(r" #[-+]?[0-9]*\.?[0-9]*[;]")
    regex3 = re.compile(r": ")
    new = regex1.sub(":", bppnewick)
    new = regex2.sub(";", new)
    new = regex3.sub(":", new)
    return new



def return_small_clade(treenode):
    "used to produce balanced trees, returns a tip node from the smaller clade"
    node = treenode
    while 1:
        if node.children:
            c1, c2 = node.children
            node = sorted([c1, c2], key=lambda x: len(x.get_leaves()))[0]
        else:
            return node



# TODO: would be useful for (eg., root) to have option to return not mrca, 
# and fuzzy match just tips, or nodes, etc...



class NodeAssist:
    """
    Given a search query (list of names, wildcard or regex) a node or list of 
    names can be retrieved under a set of pre-built functions.
    """
    def __init__(self, ttree, names, wildcard, regex):

        # attributes
        self.ttree = ttree
        self.names = names
        self.wildcard = wildcard
        self.regex = regex

        # require arguments
        if not any([names, wildcard, regex]):
            raise ToytreeError(
                "Must enter a name list, wildcard selector, or regex pattern")

        if len([i for i in [names, wildcard, regex] if i]) != 1:
            raise ToytreeError(
                "Only one method allowed at a time for: name list, wildcard selector, or regex pattern")

        # matched values
        self.nodes = []
        self.tipnames = []
        self.match_query()

        # default options to be updated in function calls
        self.mrca = True
        self.monophyletic = True


    def match_query(self):
        """
        Get list of **nodes** from {list, wildcard, or regex}
        """
        tips = []
        if self.names:

            # allow tips to be entered instead of a list
            if isinstance(self.names, (str, int)):
                self.names = [self.names]
            
            # report any names entered that seem like typos
            bad = [i for i in self.names if i not in self.ttree.get_tip_labels()]
            if any(bad):
                raise ToytreeError(
                    "Sample {} is not in the tree".format(bad))
            
            # select *nodes* that match these names
            tips = [
                i for i in self.ttree.treenode.get_leaves() 
                if i.name in self.names
            ]

        # use regex to match tipnames
        elif self.regex:
            
            # select *nodes* that regex match. Raise error if None.
            tips = [
                i for i in self.ttree.treenode.get_leaves() 
                if re.match(self.regex, i.name)
            ]               
            if not any(tips):
                raise ToytreeError("No Samples matched the regular expression")

        # use wildcard substring matching
        elif self.wildcard:
            
            # select *nodes* that match the wildcard search
            tips = [
                i for i in self.ttree.treenode.get_leaves()
                if self.wildcard in i.name
            ]
            if not any(tips):
                raise ToytreeError("No Samples matched the wildcard")

        # build list of **tipnames** from matched nodes
        if not tips:
            raise ToytreeError("no matching tipnames")

        # store results
        self.nodes = tips
        self.tipnames = [i.name for i in tips]


    def match_reciprocal(self):
        # get new query names list
        alltips = set(self.ttree.get_tip_labels())
        query_tips = set(self.tipnames)
        other_tips = list(alltips - query_tips)

        # rerun query matching
        self.names = other_tips
        self.wildcard = None
        self.regex = None
        self.match_query()


    def get_nodes(self):
        return self.nodes

    def get_tipnames(self):
        return self.tipnames

    def get_mrca(self):
        if len(self.nodes) > 1:
            return self.ttree.treenode.get_common_ancestor(self.nodes)
        return self.nodes[0]

    def get_mrca_descendants(self):
        return self.get_mrca().get_leaves()

    def is_query_monophyletic(self):       
        # if multiple tips descendant from check if they're monophyletic
        if len(self.tipnames) < 2:
            return True

        mbool, mtype, mnames = (
            self.ttree.treenode.check_monophyly(
                self.tipnames, "name", ignore_missing=True)
        )
        return mbool



# def fuzzy_match_tipnames(ttree, names, wildcard, regex, mono=True, retnode=True):
def fuzzy_match_tipnames(ttree, names, wildcard, regex, mrca=True, mono=True):
    """
    Used in multiple internal functions (e.g., .root()) and .drop_tips())
    to select an internal mrca node, or multiple tipnames, using fuzzy matching
    so that every name does not need to be written out by hand.

    name: verbose list
    wildcard: matching unique string
    regex: regex expression
    mrca: return mrca node of selected tipnames. 
    mono: raise error if selected tipnames are not monophyletic    
    """
    # require arguments
    if not any([names, wildcard, regex]):
        raise ToytreeError(
            "must enter an outgroup, wildcard selector, or regex pattern")

    # get list of **nodes** from {list, wildcard, or regex}
    tips = []
    if names:
        if isinstance(names, (str, int)):
            names = [names]
        notfound = [i for i in names if i not in ttree.get_tip_labels()]
        if any(notfound):
            raise ToytreeError(
                "Sample {} is not in the tree".format(notfound))
        tips = [i for i in ttree.treenode.get_leaves() if i.name in names]

    # use regex to match tipnames
    elif regex:
        tips = [
            i for i in ttree.treenode.get_leaves() if re.match(regex, i.name)
        ]               
        if not any(tips):
            raise ToytreeError("No Samples matched the regular expression")

    # use wildcard substring matching
    elif wildcard:
        tips = [i for i in ttree.treenode.get_leaves() if wildcard in i.name]
        if not any(tips):
            raise ToytreeError("No Samples matched the wildcard")

    # build list of **tipnames** from matched nodes
    if not tips:
        raise ToytreeError("no matching tipnames")       
    tipnames = [i.name for i in tips]

    # if a single tipname matched no need to check for monophyly
    if len(tips) == 1:
        if mrca:
            return tips[0]
        else:
            return tipnames

    # if multiple nodes matched, check if they're monophyletic
    mbool, mtype, mnames = (
        ttree.treenode.check_monophyly(
            tipnames, "name", ignore_missing=True)
    )

    # get mrca node
    node = ttree.treenode.get_common_ancestor(tips)

    # raise an error if required to be monophyletic but not
    if mono:
        if not mbool:
            raise ToytreeError(
                "Taxon list cannot be paraphyletic")

    # return tips or nodes
    if not mrca:
        return tipnames
    else:
        return node
