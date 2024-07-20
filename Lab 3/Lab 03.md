# Alejandro Martínez - 21430
# Samuel Argueta - 211024

<i><u>[GRAMATICA](./program/ConfRoomScheduler.g4)</u></i>

`
antlr -Dlanguage=Python3 ConfRoomScheduler.g4 && python3 DriverConfroom.py program_test_confroom.txt
`

## 1. Cree un programa que reserve una sala de conferencias.
Modificacion
**ya existia, no es necesario modificar*
```bash
reserve: 'RESERVAR' ID 'PARA' DATE 'DE' TIME 'A' TIME ;
```
Test
```bash
RESERVAR sala101 PARA 12/12/2024 DE 07:00 A 08:00
```
## 2. Cree un programa que cancele una reserva de sala de conferencias.
Modificacion
**ya existia, no es necesario modificar*
```bash
cancel: 'CANCELAR' ID 'PARA' DATE 'DE' TIME 'A' TIME ;
```
Test
```bash
CANCELAR sala101 PARA 12/12/2024 DE 07:00 A 08:00
```
## 3. Experimente con varias reservas y cancelaciones en un mismo programa.
Test
```bash
RESERVAR sala101 PARA 12/12/2024 DE 07:00 A 08:00
CANCELAR sala101 PARA 12/12/2024 DE 07:00 A 08:00
RESERVAR sala102 PARA 01/10/2023 DE 10:00 A 12:00
```
## 4. Modifique el DSL para incluir el nombre del solicitante de la reserva.
Modificacion
```bash
reserve: 'RESERVAR' ID 'PARA' DATE 'DE' TIME 'A' TIME 'POR' NAME ; 
NAME: [a-zA-Z]+ ; 
```
Test
```bash
RESERVAR sala101 PARA 12/12/2024 DE 07:00 A 08:00 POR Alejandro
```
## 5. Agregue manejo de errores para detectar fechas u horas invalidas.
Modificacion
```bash
```
Test
```bash
```
## 6. Cree un programa que incluya reservas solapadas y verifique su manejo (para validar reservaciones traslapadas, use un listener de ANTLR en Python; el listener llevara la cuenta de las reservaciones y validara cada nueva reservacion en contra de las existentes).
Modificacion
```python
def enterReserveStat(self, ctx:ConfRoomSchedulerParser.ReserveStatContext):
	room_id = ctx.ID().getText()
	date = ctx.DATE().getText()
	start_time = ctx.TIME(0).getText()
	end_time = ctx.TIME(1).getText()
	requester = ctx.NAME().getText()
	description = ctx.DESCRIPTION().getText()

	# Check for overlapping reservations
	for res in self.reservations:
		if res['room_id'] == room_id and res['date'] == date:
			if (start_time < res['end_time'] and end_time > res['start_time']):
				print(f"Error: Reservation for {room_id} on {date} from {start_time} to {end_time} overlaps with an existing reservation.")
				return

	self.reservations.append({
		'room_id': room_id,
		'date': date,
		'start_time': start_time,
		'end_time': end_time,
		'requester': requester,
		'description': description
	})

def enterCancelStat(self, ctx:ConfRoomSchedulerParser.CancelStatContext):
	room_id = ctx.ID().getText()
	date = ctx.DATE().getText()
	start_time = ctx.TIME(0).getText()
	end_time = ctx.TIME(1).getText()
	requester = ctx.NAME().getText()

	# Find and remove the reservation
	self.reservations = [res for res in self.reservations if not (res['room_id'] == room_id and res['date'] == date and res['start_time'] == start_time and res['end_time'] == end_time and res['requester'] == requester)]
```
## 7. Extienda el DSL para soportar descripciones de eventos.
Modificacion
```bash
```
Test
```bash
```
## 8. Agregue validaciones adicionales como restricciones de tiempo de uso maximo.
Modificacion
```bash
```
Test
```bash
```
## 9. Implemente una funcionalidad para listar las reservas existentes.
Modificacion
```bash
```
Test
```bash
```
## 10. Cree un programa que utilice todas las caracterısticas extendidas del DSL.
Test
```bash
RESERVAR sala101 PARA 15/07/2024 DE 09:00 A 11:00 SOLICITADO_POR Juan DESCRIPCION Reunión de equipo
RESERVAR sala102 PARA 16/07/2024 DE 10:00 A 12:00 SOLICITADO_POR María DESCRIPCION Taller de capacitación
CANCELAR sala101 PARA 15/07/2024 DE 09:00 A 11:00 SOLICITADO_POR Juan
```
## 11. Añada soporte para diferentes tipos de salas (por ejemplo, sala de juntas, sala de capacitacion).
Modificacion
```bash
reserve: 'RESERVAR' ROOMTYPE ID 'PARA' DATE 'DE' TIME 'A' TIME 'SOLICITADO_POR' NAME 'DESCRIPCION' DESCRIPTION ;
ROOMTYPE: 'sala_de_juntas' | 'sala_de_capacitacion' ;
```
Test
```bash
```
## 12. Implemente un sistema de notificaciones para reservas proximas.
Modificacion
```bash
```
Test
```bash
```
## 13. Extienda el DSL para permitir la reprogramacion de reservas.
Modificacion
```bash
reschedule: 'REPROGRAMAR' ID 'PARA' DATE 'DE' TIME 'A' TIME 'SOLICITADO_POR' NAME ;
```
Test
```bash
REPROGRAMAR sala101 PARA 20/07/2024 DE 14:00 A 16:00 SOLICITADO_POR Juan
```
## 14. Cree un programa que reprograme una reserva existente y valide el cambio (para validar reservaciones traslapadas, use un listener de ANTLR en Python que ya creo en una actividad anterior; el listener llevara la cuenta de las reservaciones y validara cada nueva reservacion en contra de las existentes).
Modificacion
```bash
```
Test
```bash
```