/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2015/8/1 19:21:42                            */
/*==============================================================*/


drop table if exists ad;

drop table if exists goods;

drop table if exists list;

drop table if exists style;

drop table if exists user;

/*==============================================================*/
/* Table: ad                                                    */
/*==============================================================*/
create table ad
(
   ad_id                int not null,
   username             varchar(50) not null,
   adpassword           varchar(50) not null,
   primary key (ad_id)
);

/*==============================================================*/
/* Table: goods                                                 */
/*==============================================================*/
create table goods
(
   goods_id             int not null auto_increment,
   style_id             int,
   number               int,
   name                 varchar(50),
   imageurl             varchar(50),
   detailurl            varchar(100),
   price                decimal(10,2),
   introduce            varchar(255),
   messagetotal         varchar(255),
   primary key (goods_id)
);

/*==============================================================*/
/* Table: list                                                  */
/*==============================================================*/
create table list
(
   list_id              int not null auto_increment,
   happentime           varchar(20),
   money                decimal(10,2),
   comment              varchar(255),
   user_id              int,
   primary key (list_id)
);

/*==============================================================*/
/* Table: style                                                 */
/*==============================================================*/
create table style
(
   style_id             int not null auto_increment,
   name                 varchar(50),
   primary key (style_id)
);

/*==============================================================*/
/* Table: user                                                  */
/*==============================================================*/
create table user
(
   user_id              int not null auto_increment,
   username             varchar(50) not null,
   userpassword         varchar(50) not null,
   phone                varchar(50) not null,
   registertime         varchar(50) not null,
   sex                  varchar(5) not null,
   address              varchar(128) not null,
   age                  int not null,
   primary key (user_id)
);

alter table goods add constraint FK_Reference_2 foreign key (style_id)
      references style (style_id) on delete restrict on update restrict;

alter table list add constraint FK_Reference_3 foreign key (user_id)
      references user (user_id) on delete restrict on update restrict;

