create table product
(
    id              int auto_increment
        primary key,
    user_id         int                                      not null,
    category        varchar(255)                             null,
    selling_price   int                                      null,
    cost_price      int                                      null,
    name            varchar(255)                             null,
    description     varchar(255)                             null,
    barcode         varchar(255)                             null,
    expiration_date datetime(6)                              null,
    size            varchar(255)                             null,
    search_keywords text                                     null,
    created_at      datetime(6) default CURRENT_TIMESTAMP(6) not null,
    updated_at      datetime(6) default CURRENT_TIMESTAMP(6) not null,
    constraint product_user_id
        foreign key (user_id) references user (id)
)
    charset = utf8;

create fulltext index product_search_keywords_idx
    on product (search_keywords);

