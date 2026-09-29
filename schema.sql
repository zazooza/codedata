-- ============================================================
--  schema.sql — ระบบฟิตเนส (นิสิตออกแบบและเขียนเอง)
--  กติกา: การจอง = M:N (member × gym_class), อุปกรณ์ต่อคลาส = M:N (gym_class × equipment),
--         แต่ละคลาสมีเทรนเนอร์ (1:M จาก trainer)
-- ============================================================
CREATE TABLE member (
	member_id		int				auto_increment	,
	name			varchar(100)	not null		,
	gender			varchar(20)						,
	phone 			varchar(20)						,
	email			varchar(100)	unique			,
	join_date		date 			not null		,
	package_type	varchar(50)						,
	constraint	mem_id_pk	primary key (member_id)	
);

CREATE TABLE trainer (
	trainer_id			int					auto_increment	,
	name 				varchar(100)		not null		,
	specialty			varchar(100)						,
	phone 				varchar(20)							,
	mentor_trainer_id	int									,
	constraint 	trai_id_pk 	primary key (trainer_id)		,
	constraint 	fk_trai_mentor foreign key (mentor_trainer_id) references trainer(trainer_id) ON DELETE SET NULL
);

CREATE TABLE gym_class (
	class_id 			int				auto_increment	,
	trainer_id			int				not null		,
	name 				varchar(100)	not null		,
	room 				varchar(20)						,
	capacity			int				not null		,
	schedule_time		datetime		not null		,
	constraint	class_id_pk	primary key (class_id)		,
	constraint 	fk_class_trainer foreign key (trainer_id) references trainer(trainer_id) ON DELETE CASCADE
);

CREATE TABLE booking (
	booking_id 		int 		auto_increment						,
	member_id 		int 		not null							,
	class_id		int			not null							,
	book_date 		datetime 	not null 							,
	status 			varchar(50)	not null default 'CONFIRMED'		,
	constraint 	book_id_pk 		primary key (booking_id)			,
	constraint	fk_booking_member	foreign key (member_id) references member(member_id) ON DELETE CASCADE,
	constraint 	fk_booking_class	foreign key (class_id) references gym_class(class_id) ON DELETE CASCADE	
);

CREATE TABLE equipment (
	equip_id 		int				auto_increment		,
	name 			varchar(50)		not null			,
	zone			varchar(50)							,
	status 			varchar(50)		not null			,
	total_quantity 	int 			not null			,
	constraint 	equip_id_pk	primary key (equip_id)	
);

CREATE TABLE class_equipment (
	class_id		int 	not null			,
	equip_id 		int 	not null			,
	quantity		int 	not null			,
	constraint	ce_pk			primary key (class_id, equip_id),
	constraint	fk_ce_class 	foreign key (class_id) references gym_class(class_id) ON DELETE CASCADE,
	constraint	fk_ce_equip 	foreign key (equip_id) references equipment(equip_id) ON DELETE CASCADE
);
-- ============================================================
-- 						INSERT 
-- ============================================================
INSERT INTO member (name, gender, phone, email, join_date, package_type) VALUES 
('Alex Johnson', 'Male', '0812345678', 'alex.j@email.com', '2026-01-15', 'VIP Annual'),
('Emily Watson', 'Female', '0898765432', 'emily.w@email.com', '2026-02-01', 'Monthly Pass'),
('Daniel Smith', 'Male', '0821112223', 'daniel.s@email.com', '2026-02-10', 'Student Pass'),
('Sophia Martinez', 'Female', '0854443322', 'sophia.m@email.com', '2026-03-05', 'VIP Annual'),
('Michael Brown', 'Male', '0867778899', 'michael.b@email.com', '2026-03-20', 'Monthly Pass'),
('Jessica Taylor', 'Female', NULL, 'jessica.t@email.com', '2026-04-01', 'Monthly Pass'),
('David Wilson', 'Male', '0839990011', NULL, '2026-04-12', 'Student Pass'),
('Olivia Anderson', 'Female', '0882223344', 'olivia.a@email.com', '2026-05-01', 'VIP Annual'),
('James Thomas', 'Male', '0875556677', 'james.t@email.com', '2026-05-18', 'Monthly Pass'),
('Robert White', 'Male', NULL, NULL, '2026-06-02', 'Student Pass');

INSERT INTO trainer (name, specialty, phone, mentor_trainer_id) VALUES 
('Chris Hemsworth', 'Bodybuilding & Powerlifting', '0811112222', NULL), 
('Serena Williams', 'Cardio & Endurance', '0822223333', NULL),        
('Marcus Vance', 'CrossFit & Functional Training', '0833334444', 1),   
('Elena Rostova', 'Yoga & Pilates', '0844445555', 2),                 
('John Miller', 'Boxing & HIIT', '0855556666', 1),                    
('Sarah Jenkins', 'Weight Loss & Nutrition', NULL, 2);  

INSERT INTO gym_class (trainer_id, name, room, capacity, schedule_time) VALUES 
(1, 'Power Weightlifting', 'Room A', 15, '2026-10-01 09:00:00'),
(2, 'Cardio Burn', 'Studio 1', 20, '2026-10-01 10:30:00'),
(3, 'CrossFit Challenge', 'Zone X', 12, '2026-10-01 14:00:00'),
(4, 'Morning Yoga', 'Studio 2', 15, '2026-10-02 08:00:00'),
(5, 'Boxing Basics', 'Ring Zone', 10, '2026-10-02 16:00:00'),
(6, 'Fat Loss HIIT', 'Studio 1', 18, '2026-10-03 17:00:00');

INSERT INTO booking (member_id, class_id, book_date, status) VALUES 
(1, 1, '2026-09-25 08:30:00', 'CONFIRMED'),
(2, 2, '2026-09-25 09:15:00', 'CONFIRMED'),
(3, 1, '2026-09-25 10:00:00', 'CONFIRMED'),
(4, 4, '2026-09-26 11:20:00', 'CONFIRMED'),
(5, 3, '2026-09-26 14:00:00', 'CONFIRMED'),
(6, 5, '2026-09-27 09:00:00', 'CANCELLED'),
(7, 2, '2026-09-27 10:30:00', 'CONFIRMED'),
(8, 6, '2026-09-28 15:45:00', 'CONFIRMED');

INSERT INTO equipment (name, zone, status, total_quantity) VALUES 
('Dumbbell Set 10kg', 'Free Weight', 'Available', 20),
('Yoga Mat', 'Studio Zone', 'Available', 30),
('Boxing Gloves Pair', 'Combat Zone', 'Available', 15),
('Kettlebell 16kg', 'Free Weight', 'Available', 12),
('Jump Rope', 'Cardio Zone', 'Available', 25),
('Resistance Band', 'Studio Zone', 'Available', 40);


INSERT INTO class_equipment (class_id, equip_id, quantity) VALUES 
(1, 1, 15), -- Class 1 uses Dumbbell
(1, 4, 10), -- Class 1 uses Kettlebell
(2, 5, 20), -- Class 2 uses Jump Rope
(3, 4, 12), -- Class 3 uses Kettlebell
(4, 2, 15), -- Class 4 uses Yoga Mat
(4, 6, 15), -- Class 4 uses Resistance Band
(5, 3, 10), -- Class 5 uses Boxing Gloves
(6, 5, 18); -- Class 6 uses Jump Rope
