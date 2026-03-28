import { faker } from "@faker-js/faker";
import { User } from "#/classes/user.ts";
import { writeFile, mkdir } from "node:fs/promises";
import { join } from "node:path";
faker.seed(123);

const list: User[] = [];

for (let i = 0; i < 100; i++) {
  list.push(new User());
}

await mkdir(join("db"), { recursive: true })
await writeFile(join("db", "users.json"), JSON.stringify(list, null, 2));
