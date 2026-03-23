import { fa, Faker, faker } from "@faker-js/faker";
import { User } from "#/classes/user.ts";
import { writeFile } from "node:fs/promises";
import { join } from "node:path";
faker.seed(123);

const list: User[] = [];

for (let i = 0; i < 100; i++) {
  list.push(new User());
}

await writeFile(join("db", "users.json"), JSON.stringify(list, null, 2));
