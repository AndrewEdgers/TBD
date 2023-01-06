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

CREATE TABLE IF NOT EXISTS `giveaways`(
    `giveaway_id` varchar(20) NOT NULL,
    `message_id` varchar(20) NOT NULL,
    `channel_id` varchar(20) NOT NULL,
    `guild_id` varchar(20) NOT NULL,
    `prize` varchar(255) NOT NULL,
    `time` int(11) NOT NULL,
    `winners` int(11) NOT NULL,
    `provider` varchar(255) NOT NULL,
    `message` varchar(255) NOT NULL,
    `finished` BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS `participants`(
    `giveaway_id` varchar(20) NOT NULL,
    `user_id` varchar(20) NOT NULL,
    `entry` int(11) NOT NULL DEFAULT '0',
    `is_winner` INTEGER DEFAULT 0
);
