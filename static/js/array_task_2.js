// Base Class
class StudentBase {
  constructor(firstName, lastName, patronymic, gender, age, year) {
    this.firstName = firstName;
    this.lastName = lastName;
    this.patronymic = patronymic;
    this.gender = gender;
    this.age = age;
    this.year = year;
  }

  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  }

  set fullName(name) {
    const parts = name.split(" ");
    this.firstName = parts[0];
    this.lastName = parts[1];
  }
}

// Descendant Class
class StudentManager extends StudentBase {
  constructor() {
    super();
    this.students = [
      new StudentBase("John", "Doe", "Smith", "male", 20, 1),
      new StudentBase("Jane", "Doe", "Johnson", "female", 21, 2),
      new StudentBase("Alice", "Smith", "Brown", "female", 19, 1),
      new StudentBase("Bob", "Johnson", "Davis", "male", 22, 3),
    ]; // Array to hold student objects
  }

  // Method to add a student from HTML form input
  addStudentFromForm() {
    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;
    const patronymic = document.getElementById("patronymic").value;
    const gender = document.getElementById("gender").value;
    const age = parseInt(document.getElementById("age").value);
    const year = parseInt(document.getElementById("year").value);

    const newStudent = new StudentBase(
      firstName,
      lastName,
      patronymic,
      gender,
      age,
      year
    );
    this.students.push(newStudent);

    this.displayStudents(); // Update the student list display
    this.displayResult(); // Update the result display
  }

  // Method to display all students in the 'studentList' div
  displayStudents() {
    const studentList = document.getElementById("studentList");
    studentList.innerHTML = ""; // Clear the list

    if (this.students.length === 0) {
      studentList.textContent = "No students added yet.";
      return;
    }

    this.students.forEach((student, index) => {
      const studentDiv = document.createElement("div");
      studentDiv.textContent = `${index + 1}. ${student.fullName}, Age: ${
        student.age
      }, Year: ${student.year}, Gender: ${student.gender}`;
      studentList.appendChild(studentDiv);
    });
  }

  calculateMalePercentage() {
    const yearCounts = {}; // { year: { male: count, total: count } }

    // Count male and total students per year
    this.students.forEach((student) => {
      const year = student.year;
      if (!yearCounts[year]) yearCounts[year] = { male: 0, total: 0 };

      if (student.gender === "male") yearCounts[year].male += 1;
      yearCounts[year].total += 1;
    });

    // Find year with the highest male percentage
    let maxPercentage = 0;
    let maxYear = null;
    for (let year in yearCounts) {
      const percentage = (yearCounts[year].male / yearCounts[year].total) * 100;
      if (percentage > maxPercentage) {
        maxPercentage = percentage;
        maxYear = year;
      }
    }

    return maxYear
      ? `${maxYear} (${maxPercentage.toFixed(2)}% male)`
      : "No data available";
  }

  // Display the result in the 'result' div
  displayResult() {
    const resultDiv = document.getElementById("result");
    const year = this.calculateMalePercentage();
    resultDiv.textContent = `The year with the highest percentage of male students is: ${year}`;
  }

  // Getters and Setters
  get allStudents() {
    return this.students;
  }

  set allStudents(students) {
    this.students = students;
  }
}

// Initialize the manager instance
const manager = new StudentManager();
manager.displayStudents();
manager.displayResult();
