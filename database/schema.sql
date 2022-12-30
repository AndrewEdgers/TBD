CREATE TABLE IF NOT EXISTS `blacklist` (
  `user_id` varchar(20) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `warns` (
  `id` int(11) NOT NULL,
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `moderator_id` varchar(20) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `economy` (
    `user_id` varchar(20) NOT NULL,
    `server_id` varchar(20) NOT NULL,
    `balance` int(11) NOT NULL DEFAULT '0'
);



CREATE TABLE IF NOT EXISTS `levels`(
    `user_id` varchar(20) NOT NULL,
    `server_id` varchar(20) NOT NULL,
    `level` int(11) NOT NULL DEFAULT '0',
    `xp` int(11) NOT NULL DEFAULT '0'
);
