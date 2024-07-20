# Generated from ConfRoomScheduler.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
	from .ConfRoomSchedulerParser import ConfRoomSchedulerParser
else:
	from ConfRoomSchedulerParser import ConfRoomSchedulerParser

# This class defines a complete listener for a parse tree produced by ConfRoomSchedulerParser.
class ConfRoomSchedulerListener(ParseTreeListener):
	def __init__(self):
		self.reservations = {}

	# Enter a parse tree produced by ConfRoomSchedulerParser#prog.
	def enterProg(self, ctx:ConfRoomSchedulerParser.ProgContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#prog.
	def exitProg(self, ctx:ConfRoomSchedulerParser.ProgContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#reserveStat.
	def enterReserveStat(self, ctx:ConfRoomSchedulerParser.ReserveStatContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#reserveStat.
	def exitReserveStat(self, ctx:ConfRoomSchedulerParser.ReserveStatContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#cancelStat.
	def enterCancelStat(self, ctx:ConfRoomSchedulerParser.CancelStatContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#cancelStat.
	def exitCancelStat(self, ctx:ConfRoomSchedulerParser.CancelStatContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#rescheduleStat.
	def enterRescheduleStat(self, ctx:ConfRoomSchedulerParser.RescheduleStatContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#rescheduleStat.
	def exitRescheduleStat(self, ctx:ConfRoomSchedulerParser.RescheduleStatContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#listStat.
	def enterListStat(self, ctx:ConfRoomSchedulerParser.ListStatContext):
		print("Existing Reservations:")
		for date, reservations in self.reservations.items():
			for res in reservations:
				print(f"{res['room_type']} with ID {res['id']} on {date} from {res['start_time']} to {res['end_time']} by {res['applicant']}")


	# Exit a parse tree produced by ConfRoomSchedulerParser#listStat.
	def exitListStat(self, ctx:ConfRoomSchedulerParser.ListStatContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#blank.
	def enterBlank(self, ctx:ConfRoomSchedulerParser.BlankContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#blank.
	def exitBlank(self, ctx:ConfRoomSchedulerParser.BlankContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#reserve.
	def enterReserve(self, ctx:ConfRoomSchedulerParser.ReserveContext):
		room_type = ctx.ROOMTYPE().getText()
		res_id = ctx.ID().getText()
		date = ctx.DATE().getText()
		start_time = ctx.TIME(0).getText()
		end_time = ctx.TIME(1).getText()
		applicant = ctx.NAME().getText()
		
		if date not in self.reservations:
			self.reservations[date] = []
		
		# Check for overlapping reservations
		for res in self.reservations[date]:
			if res['id'] == res_id and self.is_overlap(start_time, end_time, res['start_time'], res['end_time']):
				print(f"Error: Overlapping reservation for ID {res_id} on {date}")
				return

		self.reservations[date].append({
			'id': res_id,
			'room_type': room_type,
			'start_time': start_time,
			'end_time': end_time,
			'applicant': applicant
		})
		print(f"Reserved {room_type} with ID {res_id} on {date} from {start_time} to {end_time} by {applicant}")

	# Exit a parse tree produced by ConfRoomSchedulerParser#reserve.
	def exitReserve(self, ctx:ConfRoomSchedulerParser.ReserveContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#cancel.
	def enterCancel(self, ctx:ConfRoomSchedulerParser.CancelContext):
		res_id = ctx.ID().getText()
		date = ctx.DATE().getText()
		start_time = ctx.TIME(0).getText()
		end_time = ctx.TIME(1).getText()

		if date in self.reservations:
			self.reservations[date] = [res for res in self.reservations[date] if not (res['id'] == res_id and res['start_time'] == start_time and res['end_time'] == end_time)]
			print(f"Cancelled reservation with ID {res_id} on {date} from {start_time} to {end_time}")
		else:
			print(f"No reservation found with ID {res_id} on {date} from {start_time} to {end_time}")

	# Exit a parse tree produced by ConfRoomSchedulerParser#cancel.
	def exitCancel(self, ctx:ConfRoomSchedulerParser.CancelContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#reschedule.
	def enterReschedule(self, ctx:ConfRoomSchedulerParser.RescheduleContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#reschedule.
	def exitReschedule(self, ctx:ConfRoomSchedulerParser.RescheduleContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#list.
	def enterList(self, ctx:ConfRoomSchedulerParser.ListContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#list.
	def exitList(self, ctx:ConfRoomSchedulerParser.ListContext):
		pass


	def is_overlap(self, start1, end1, start2, end2):
		return not (end1 <= start2 or start1 >= end2)

del ConfRoomSchedulerParser