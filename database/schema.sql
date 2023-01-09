create TABLE IF NOT EXISTS `blacklist` (
    `user_id` varchar(20) NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create TABLE IF NOT EXISTS `warns` (
    `id` int(11) NOT NULL,
    `user_id` varchar(20) NOT NULL,
    `server_id` varchar(20) NOT NULL,
    `moderator_id` varchar(20) NOT NULL,
    `reason` varchar(255) NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

create TABLE IF NOT EXISTS `economy` (
    `user_id` varchar(20) NOT NULL,
    `server_id` varchar(20) NOT NULL,
    `balance` int(11) NOT NULL DEFAULT '0'
);

create TABLE IF NOT EXISTS `levels`(
    `user_id` varchar(20) NOT NULL,
    `server_id` varchar(20) NOT NULL,
    `level` int(11) NOT NULL DEFAULT '0',
    `xp` int(11) NOT NULL DEFAULT '0'
);

create TABLE IF NOT EXISTS `giveaways`(
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

create TABLE IF NOT EXISTS `participants`(
    `giveaway_id` varchar(20) NOT NULL,
    `user_id` varchar(20) NOT NULL,
    `entry` int(11) NOT NULL DEFAULT '0',
    `is_winner` INTEGER DEFAULT 0
);

create TABLE IF NOT EXISTS `totals`(
    `guild_id` varchar(20) NOT NULL,
    `inviter_id` varchar(20) NOT NULL,
    `normal` int(11) NOT NULL DEFAULT '0',
    `left` int(11) NOT NULL DEFAULT '0',
    `fake` int(11) NOT NULL DEFAULT '0',
    PRIMARY KEY (`guild_id`, `inviter_id`)
);

create TABLE IF NOT EXISTS `invites`(
    `guild_id` varchar(20) NOT NULL,
    `code` varchar(20) NOT NULL,
    `uses` int(11) NOT NULL DEFAULT '0',
    PRIMARY KEY (`guild_id`, `code`)
);

create TABLE IF NOT EXISTS `joined`(
    `guild_id` varchar(20) NOT NULL,
    `inviter_id` varchar(20) NOT NULL,
    `joined_id` varchar(20) NOT NULL,
    PRIMARY KEY (`guild_id`, `inviter_id`, `joined_id`)
);

