create TABLE keywords(
    userID bigint,
    keyword text
);

create TABLE prefix(
    guildID bigint primary key,
    prefix VARCHAR(50)
);

create TABLE usersettings(
    userid bigint primary key,
    owntrigger boolean default true,
    quotetrigger boolean default true,
    embedmessage boolean default false
);

create TABLE textfilters(
    userid bigint,
    textfilter text
);

create TABLE channelfilters(
    userid bigint,
    channelfilter BIGINT,
    PRIMARY KEY (userid, channelfilter)
);

create TABLE serverfilters(
    userid bigint,
    serverfilter BIGINT,
    PRIMARY KEY (userid, serverfilter)
);

