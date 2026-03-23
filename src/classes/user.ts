import { faker } from "@faker-js/faker";

interface IUser {
  name: string;
  username: string;
  email: string;
  age: number;
  genere: string;
}

let i = 1;

export class User {
  id = i++;
  firstname = faker.person.firstName();
  lastname = faker.person.lastName();
  username: string;
  age = faker.number.int({ min: 13, max: 100 });
  email: string;

  constructor() {
    this.username = faker.internet.username({
      firstName: this.firstname,
      lastName: this.lastname,
    });
    this.email = faker.internet.email({
      firstName: this.firstname,
      lastName: this.lastname,
    });
  }
}
