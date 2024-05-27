create table user
(
    id         int auto_increment
        primary key,
    user_phone varchar(255)                             null,
    password   varchar(255)                             null,
    is_session tinyint(1)  default 0                    null,
    created_at datetime(6) default CURRENT_TIMESTAMP(6) not null,
    updated_at datetime(6) default CURRENT_TIMESTAMP(6) not null
);

