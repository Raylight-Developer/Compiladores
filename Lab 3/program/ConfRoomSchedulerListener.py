# Generated from ConfRoomScheduler.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
	from .ConfRoomSchedulerParser import ConfRoomSchedulerParser
else:
	from ConfRoomSchedulerParser import ConfRoomSchedulerParser

from datetime import datetime, timedelta

# This class defines a complete listener for a parse tree produced by ConfRoomSchedulerParser.
class ConfRoomSchedulerListener(ParseTreeListener):
	def __init__(self):
		self.MAX_RESERVATION_HOURS = 4
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
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#listStat.
	def exitListStat(self, ctx:ConfRoomSchedulerParser.ListStatContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#notifyStat.
	def enterNotifyStat(self, ctx:ConfRoomSchedulerParser.NotifyStatContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#notifyStat.
	def exitNotifyStat(self, ctx:ConfRoomSchedulerParser.NotifyStatContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#blank.
	def enterBlank(self, ctx:ConfRoomSchedulerParser.BlankContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#blank.
	def exitBlank(self, ctx:ConfRoomSchedulerParser.BlankContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#reserve.
	def enterReserve(self, ctx:ConfRoomSchedulerParser.ReserveContext):
		try:
			room_type = ctx.ROOMTYPE().getText()
			res_id = ctx.ID().getText()
			date = ctx.DATE().getText()
			start_time = ctx.TIME(0).getText()
			end_time = ctx.TIME(1).getText()
			applicant = ctx.NAME().getText()
			description = ctx.DESCRIPTION().getText() if ctx.DESCRIPTION() else None

			# Validate date and time formats
			res_date = datetime.strptime(date, "%d/%m/%Y")
			res_start = datetime.strptime(f"{date} {start_time}", "%d/%m/%Y %H:%M")
			res_end = datetime.strptime(f"{date} {end_time}", "%d/%m/%Y %H:%M")

			# Check for invalid times
			if res_start >= res_end:
				print(f"Error: Start time must be before end time for reservation {res_id}")
				return

			# Check for maximum reservation duration
			if (res_end - res_start).total_seconds() > self.MAX_RESERVATION_HOURS * 3600:
				print(f"Error: Reservation {res_id} exceeds maximum allowed duration of {self.MAX_RESERVATION_HOURS} hours")
				return

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
				'applicant': applicant,
				'description': description
			})
			print(f"Reserved {room_type} with ID {res_id} on {date} from {start_time} to {end_time} by {applicant}" + (f" with description {description}" if description else ""))

		except ValueError as e:
			print(f"Error: Invalid date or time format in reservation {res_id}")

	# Exit a parse tree produced by ConfRoomSchedulerParser#reserve.
	def exitReserve(self, ctx:ConfRoomSchedulerParser.ReserveContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#cancel.
	def enterCancel(self, ctx:ConfRoomSchedulerParser.CancelContext):
		pass

	# Exit a parse tree produced by ConfRoomSchedulerParser#cancel.
	def exitCancel(self, ctx:ConfRoomSchedulerParser.CancelContext):
		res_id = ctx.ID().getText()
		date = ctx.DATE().getText()
		start_time = ctx.TIME(0).getText()
		end_time = ctx.TIME(1).getText()

		if date in self.reservations:
			self.reservations[date] = [res for res in self.reservations[date] if not (res['id'] == res_id and res['start_time'] == start_time and res['end_time'] == end_time)]
			print(f"Cancelled reservation with ID {res_id} on {date} from {start_time} to {end_time}")
		else:
			print(f"No reservation found with ID {res_id} on {date} from {start_time} to {end_time}")


	# Enter a parse tree produced by ConfRoomSchedulerParser#reschedule.
	def enterReschedule(self, ctx:ConfRoomSchedulerParser.RescheduleContext):
		try:
			res_id = ctx.ID().getText()
			old_date = ctx.DATE(0).getText()
			new_date = ctx.DATE(1).getText()
			new_start_time = ctx.TIME(0).getText()
			new_end_time = ctx.TIME(1).getText()

			# Validate date and time formats
			new_res_start = datetime.strptime(f"{new_date} {new_start_time}", "%d/%m/%Y %H:%M")
			new_res_end = datetime.strptime(f"{new_date} {new_end_time}", "%d/%m/%Y %H:%M")

			# Check for invalid times
			if new_res_start >= new_res_end:
				print(f"Error: Start time must be before end time for rescheduled reservation {res_id}")
				return

			# Check for maximum reservation duration
			if (new_res_end - new_res_start).total_seconds() > self.MAX_RESERVATION_HOURS * 3600:
				print(f"Error: Rescheduled reservation {res_id} exceeds maximum allowed duration of {self.MAX_RESERVATION_HOURS} hours")
				return

			# Find and remove the old reservation
			if old_date in self.reservations:
				old_res = None
				for res in self.reservations[old_date]:
					if res['id'] == res_id:
						old_res = res
						break
				if old_res:
					self.reservations[old_date].remove(old_res)
				else:
					print(f"Error: No reservation found with ID {res_id} on {old_date}")
					return
			else:
				print(f"Error: No reservation found with ID {res_id} on {old_date}")
				return

			if new_date not in self.reservations:
				self.reservations[new_date] = []

			# Check for overlapping reservations
			for res in self.reservations[new_date]:
				if res['id'] == res_id and self.is_overlap(new_start_time, new_end_time, res['start_time'], res['end_time']):
					print(f"Error: Overlapping reservation for ID {res_id} on {new_date}")
					return

			self.reservations[new_date].append({
				'id': res_id,
				'room_type': old_res['room_type'],
				'start_time': new_start_time,
				'end_time': new_end_time,
				'applicant': old_res['applicant'],
				'description': old_res['description']
			})
			print(f"Rescheduled reservation with ID {res_id} to {new_date} from {new_start_time} to {new_end_time}")

		except ValueError as e:
			print(f"Error: Invalid date or time format in rescheduling reservation {res_id}")


	# Exit a parse tree produced by ConfRoomSchedulerParser#reschedule.
	def exitReschedule(self, ctx:ConfRoomSchedulerParser.RescheduleContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#list.
	def enterList(self, ctx:ConfRoomSchedulerParser.ListContext):
		print("Existing Reservations:")
		for date, reservations in self.reservations.items():
			for res in reservations:
				print(f"{res['room_type']} with ID {res['id']} on {date} from {res['start_time']} to {res['end_time']} by {res['applicant']}")

	# Exit a parse tree produced by ConfRoomSchedulerParser#list.
	def exitList(self, ctx:ConfRoomSchedulerParser.ListContext):
		pass


	# Enter a parse tree produced by ConfRoomSchedulerParser#notify.
	def enterNotify(self, ctx:ConfRoomSchedulerParser.NotifyContext):
		current_time = datetime.now()
		upcoming_time = current_time + timedelta(hours=24)
		print("Upcoming Reservations within 24 hours:")
		res_count = 0
		for date, reservations in self.reservations.items():
			for res in reservations:
				res_start = datetime.strptime(f"{date} {res['start_time']}", "%d/%m/%Y %H:%M")
				if current_time <= res_start <= upcoming_time:
					res_count += 1
					print(f"{res['room_type']} with ID {res['id']} on {date} from {res['start_time']} to {res['end_time']} by {res['applicant']}")
		if (res_count == 0):
			print("None")

	# Exit a parse tree produced by ConfRoomSchedulerParser#notify.
	def exitNotify(self, ctx:ConfRoomSchedulerParser.NotifyContext):
		pass


del ConfRoomSchedulerParser