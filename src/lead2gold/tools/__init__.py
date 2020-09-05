#author: plachta11b (janholcak@gmail.com)

# Tools

from .tool import Tool
from .graphprot import GraphProt
from .homer import Homer
from .meme import MEME
from .mcat import MCAT
from .mds import MDS
from .consensus import Consensus
from .sshmm import ssHMM
from .weeder import Weeder
from .zagros import Zagros
from .rpmcmc import RPMCMC
from .alignace import AlignACE
from .emd import EMD
from .transfac import TRANSFAC
from .transfaclike import TRANSFAClike
from .pwm_horizontal import PWM_horizontal
from .pwm_vertical import PWM_vertical
from .pfm_horizontal import PFM_horizontal
from .ppm_horizontal import PPM_horizontal
# from .pfm_vertical import PFM_vertical

def get_tool(name):
	"""
	Returns an instance of a specific tool.
	Parameters
	----------
	name : str
		Name of the tool (case-insensitive).
	Returns
	-------
	tool : Tool instance
	"""
	tool_name = name.lower()
	tool = None
	for cls in Tool.__subclasses__():
		if tool_name == cls.toolName.lower():
			tool = cls
	
	if tool is None:
		raise ValueError("Tool {0} not found!\n".format(name))

	return tool()
