---
title: "Nodejs连接sqlite数据库"
date: 2021-05-15T21:28:07+08:00
description: "使用niodejs操作sqlite数据库"
tags: ["SQLITE"]
featured_image: ""
# images is optional, but needed for showing Twitter Card
images: []
categories: "DB"
comment : true
---

##  编译nodejs相关模块better-sqlite3

1. 安装 [windows-build-tools](https://github.com/felixrieseberg/windows-build-tools)， 注意用管理员身份启动终端（如果安装node的时侯已经安装了相关的tools就略过这一步）

```
npm install --global windows-build-tools
```

 这里有个点要注意一下，这个工具分版本 vs2015, vs2017， 默认是2017，如果是需要2015版安装时后面加参数

```
npm install --global windows-build-tools --vs2015
```

如果不知道当前需要哪个版本，先默认安装，后面编译出错会报出来

2. 安装 better-sqlite3

```
npm install better-sqlite3
```

  如果顺利这里就成功了。

  这里有情况

  node-gyp报错，仔细看一下，如果是visual studio 工具问题，基本上是版本原因，回第一步

  如果只是node-gyp错误

``` 
npm uninstall node-gyp -g
npm install -g node-gyp
```

  然后再执行安装命令，需要注意，少数情况下node版本也会造成编译失败。  

3. 启动 electron 并调用 better-sqlite3  

const DB = require('better-sqlite3');

  这里还有个可能的报错，编译的node版本对不上，需要使用 electron-rebuild

npm install --save-dev electron-rebuild

    ./node_modules/.bin/electron-rebuild
    # 在windows下如果上述命令遇到了问题，尝试这个：
    .\node_modules\.bin\electron-rebuild.cmd

 这个特别慢， 而且到最后我也没成功， 所以用了别的命令

```npm
electron-rebuild -f -w better-sqlite3
```

或者在package.json的scripts中加入并运行这个

```json
"rebuild": "electron-rebuild -f -w better-sqlite3",
```

## better-sqlite3基础操作：[API](https://github.com/JoshuaWise/better-sqlite3/blob/HEAD/docs/api.md)

> ### new Database(path, [options])
>
> 创建一个新的数据库连接。 如果数据库文件不存在，则会创建它。 这是同步发生的，这意味着您可以立即开始执行查询。 您可以创建一个 [内存数据库 ](https://www.sqlite.org/inmemorydb.html)通过传递 `":memory:"`作为第一个论点。 
>
> > 还可以通过传递由返回的缓冲区来创建内存数据库 [`.serialize()`](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#serializeoptions---buffer)，而不是将字符串作为第一个参数传递。 
>
> 接受各种选项： 
>
> - `options.readonly`：以只读模式打开数据库连接（默认值： `false`). 
> - `options.fileMustExist`：如果数据库不存在，则 `Error`将被抛出，而不是创建一个新文件。  此选项不影响内存中或只读数据库连接（默认值： `false`). 
> - `options.timeout`：在对锁定的数据库执行查询之前，在引发查询前要等待的毫秒数 `SQLITE_BUSY`错误（默认值： `5000`). 
> - `options.verbose`：提供一个由数据库连接执行的每个SQL字符串调用的函数（默认值： `null`). 
>
> ```js
> const Database = require('better-sqlite3');
> const db = new Database('foobar.db', { verbose: console.log });
> ```

### .prepare(*string*) -> Statement

创建一个新的准备 [`Statement`](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#class-statement)从给定的SQL字符串。 

```js
const stmt = db.prepare('SELECT name, age FROM cats');
```

### .transaction(*function*) -> *function*

创建一个始终在 内部运行的函数 [事务 ](https://sqlite.org/lang_transaction.html)。 调用该函数时，它将开始新的事务。 当函数返回时，事务将被提交。 如果抛出异常，则事务将回滚（并且异常将照常传播）。 

```js
const insert = db.prepare('INSERT INTO cats (name, age) VALUES (@name, @age)');

const insertMany = db.transaction((cats) => {
  for (const cat of cats) insert.run(cat);
});

insertMany([
  { name: 'Joey', age: 2 },
  { name: 'Sally', age: 4 },
  { name: 'Junior', age: 1 },
]);
```

可以从其他事务功能内部调用事务功能。 这样做时，内部事务将成为一个 [保存点 ](https://www.sqlite.org/lang_savepoint.html)。 

```js
const newExpense = db.prepare('INSERT INTO expenses (note, dollars) VALUES (?, ?)');

const adopt = db.transaction((cats) => {
  newExpense.run('adoption fees', 20);
  insertMany(cats); // nested transaction
});
```

### .exec(*string*) -> **this**

执行给定的SQL字符串。 与 不同 [准备好的语句 ](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#preparestring---statement)，它可以执行包含多个SQL语句的字符串。 与使用 相比，此函数执行效果较差且安全性较低 [准备好的语句 ](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#preparestring---statement)。 仅当需要从外部源（通常是文件）执行SQL时，才应使用此方法。 如果发生错误，则执行停止，并且不再执行其他语句。 您必须手动回滚更改。 

```js
const migration = fs.readFileSync('migrate-schema.sql', 'utf8');
db.exec(migration);
```

### .close（）-> *此*

关闭数据库连接。  调用此方法后，将无法创建或执行任何语句。

### .run([*...bindParameters*]) -> *object*

执行准备好的语句。  执行完成后，它会返回一个 `info`描述所做任何更改的对象。  这 `info`对象具有两个属性： 

- `info.changes`：此操作插入，更新或删除的总行数。 更改 [外键动作 ](https://www.sqlite.org/foreignkeys.html#fk_actions)或 [触发程序 ](https://www.sqlite.org/lang_createtrigger.html)所做的 不计算在内。 
- `info.lastInsertRowid`： 的 [rowid ](https://www.sqlite.org/lang_createtable.html#rowid)插入数据库的最后一行 （忽略那些由 引起的行 [触发器程序 ](https://www.sqlite.org/lang_createtrigger.html)）。 如果当前语句未在数据库中插入任何行，则应完全忽略该数字。 

如果执行该语句失败，则 `Error`被抛出。 

您可以指定 [bind参数 ](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#binding-parameters)，仅对给定执行绑定。 

```js
const stmt = db.prepare('INSERT INTO cats (name, age) VALUES (?, ?)');
const info = stmt.run('Joey', 2);

console.log(info.changes); // => 1
```

### .get([*...bindParameters*]) -> *row*

\* *（仅适用于返回数据的语句）* 

执行准备好的语句。  执行完成后，它将返回一个对象，该对象代表查询检索的第一行。  对象的键代表列名。 

如果该语句成功但没有找到数据， `undefined`返回。  如果执行该语句失败，则 `Error`被抛出。 

您可以指定 [bind参数 ](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#binding-parameters)，仅对给定执行绑定。 

```js
const stmt = db.prepare('SELECT age FROM cats WHERE name = ?');
const cat = stmt.get('Joey');

console.log(cat.age); // => 2
```

### .all([*...bindParameters*]) -> *array of rows*

\* *（仅适用于返回数据的语句）* 

如同 `.get()`，而不是仅检索一行，而是将检索所有匹配的行。  返回值是一个行对象数组。 

如果未找到任何行，则该数组将为空。  如果执行该语句失败，则 `Error`被抛出。 

您可以指定 [bind参数 ](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#binding-parameters)，仅对给定执行绑定。 

```js
const stmt = db.prepare('SELECT * FROM cats WHERE name = ?');
const cats = stmt.all('Joey');

console.log(cats.length); // => 1
```

### .iterate([*...bindParameters*]) -> *iterator*

\* *（仅适用于返回数据的语句）* 

如同 [`.all()`](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#allbindparameters---array-of-rows)，但返回的是 ，而不是一起返回每一行， 一个一行地 [迭代器 ](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols)因此您可以 检索行。 如果您打算无论如何都要检索每一行， [`.all()`](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#allbindparameters---array-of-rows)会稍微好一些。 

如果执行该语句失败，则 `Error`被抛出并且迭代器被关闭。 

您可以指定 [bind参数 ](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md#binding-parameters)，仅对给定执行绑定。 

```js
const stmt = db.prepare('SELECT * FROM cats');

for (const cat of stmt.iterate()) {
  if (cat.name === 'Joey') {
    console.log('found him!');
    break;
  }
}
```

