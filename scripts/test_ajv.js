#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

// ajv@8.12.0
// ajv-formats@2.1.1
// ajv-formats-draft2019@1.6.1
const Ajv = require("ajv/dist/2020");
const addFormats = require("ajv-formats");
const addFormats2019 = require("ajv-formats-draft2019");

const ajv = new Ajv({
  strictSchema: false,
  allErrors: true,
});
addFormats(ajv);
addFormats2019(ajv);

function* globSync(dirname, extname) {
  const dirents = fs.readdirSync(dirname, { withFileTypes: true });
  for (const dirent of dirents) {
    if (dirent.name.endsWith(extname)) {
      yield path.join(dirent.path, dirent.name);
    }
  }
  for (const dirent of dirents) {
    if (dirent.isDirectory()) {
      const filename = path.join(dirent.path, dirent.name);
      const filenames = globSync(filename, extname);
      for (const filename of filenames) {
        yield filename;
      }
    }
  }
}

const rootDirname = path.join(__dirname, "..");
for (const filename of globSync(rootDirname, ".schema.json")) {
  ajv.addSchema(require(filename));
}

const tests = [];
const testDirname = path.join(rootDirname, "test");
for (const schemaPath of globSync(testDirname, "test.schema.json")) {
  const passDirname = path.join(schemaPath, "../pass");
  const failDirname = path.join(schemaPath, "../fail");

  for (const instancePath of globSync(passDirname, ".json")) {
    tests.push([schemaPath, instancePath]);
  }
  for (const instancePath of globSync(failDirname, ".json")) {
    tests.push([schemaPath, instancePath]);
  }
}

let exitstatus = 0;

console.log(`1..${tests.length}`);
let i = 1;
for (const [schemaPath, instancePath] of tests) {
  const schema = require(schemaPath);
  const instance = require(instancePath);

  const schemaShortPath = path.relative(rootDirname, schemaPath);
  const instanceShortPath = path.relative(rootDirname, instancePath);
  const type = path.basename(path.dirname(instancePath));

  const valid = ajv.validate(schema, instance);

  if ((type == "pass" && valid) || (type == "fail" && !valid)) {
    console.log("ok", i, "-", schemaShortPath, instanceShortPath);
  } else {
    console.log("not ok", i, "-", schemaShortPath, instanceShortPath);
    console.log(ajv.errors);
    exitstatus++;
  }

  i++;
}

process.exit(exitstatus);
