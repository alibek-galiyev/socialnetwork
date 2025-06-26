create table posts (
    id serial primary key,
    title varchar(255) not null,
    content text not null,
    published boolean default true,
    created_at timestamp default current_timestamp,
    rating integer
);