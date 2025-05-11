import React, { useState } from 'react';

const emptyStudent = {
    gender: '',
    age: '',
    department: '',
    attendance: '',
    midterm: '',
    assignments: '',
    quizzes: '',
    participation: '',
    projects: '',
    studyHours: '',
    extracurricular: '',
    internetAccess: '',
    parentEducation: '',
    stressLevel: '',
    sleepHours: '',
};

const departments = ["Computer Science", "Data Science", "Software Engineering"];
const genders = ["Male", "Female"];
const parentEducationOptions = [
    { label: 'Less than High School', value: 0 },
    { label: 'High School', value: 1 },
    { label: 'Some College', value: 2 },
    { label: "Bachelor's Degree", value: 3 },
    { label: 'Graduate Degree', value: 4 },
];

const BACKEND_URL = 'https://abba-139-135-36-24.ngrok-free.app';

const LearnLyticsForm = () => {
    const [students, setStudents] = useState([{ ...emptyStudent }]);
    const [results, setResults] = useState([]);

    const handleChange = (index, e) => {
        const { name, value } = e.target;
        const updated = [...students];
        updated[index][name] = name === 'parentEducation' ? Number(value) : value;
        setStudents(updated);
    };

    const validate = (student) => {
        const messages = [];

        const requiredFields = [
            'gender', 'age', 'attendance', 'midterm', 'assignments', 'quizzes',
            'participation', 'projects', 'studyHours', 'extracurricular', 'internetAccess',
            'parentEducation', 'stressLevel', 'sleepHours', 'department'
        ];

        const fieldLabels = {
            attendance: 'Attendance (%)',
            midterm: 'Midterm Score',
            assignments: 'Assignments Avg',
            quizzes: 'Quizzes Avg',
            participation: 'Participation Score',
            projects: 'Projects Score',
            stressLevel: 'Stress Level',
            sleepHours: 'Sleep Hours/Night',
            age: 'Age',
        };

        for (const field of requiredFields) {
            if (student[field] === '') {
                messages.push(`Field "${fieldLabels[field] || field}" is required.`);
            }
        }

        const numericFields100 = ['attendance', 'midterm', 'assignments', 'quizzes', 'participation', 'projects'];
        numericFields100.forEach(field => {
            const val = Number(student[field]);
            if (isNaN(val) || val < 0 || val > 100) {
                messages.push(`${fieldLabels[field]} must be between 0 and 100.`);
            }
        });

        const age = Number(student.age);
        if (isNaN(age) || age < 15 || age > 30) {
            messages.push('Age must be between 15 and 30.');
        }

        const stress = Number(student.stressLevel);
        if (isNaN(stress) || stress < 1 || stress > 10) {
            messages.push('Stress Level must be between 1 and 10.');
        }

        const sleepHours = Number(student.sleepHours);
        if (isNaN(sleepHours) || sleepHours < 0 || sleepHours > 24) {
            messages.push('Sleep Hours/Night must be between 0 and 24.');
        }

        return messages;
    };


    const handleSubmit = async () => {
        const student = students[0];
        const validationErrors = validate(student);

        if (validationErrors.length > 0) {
            alert(validationErrors.join('\n')); // Show alert with validation errors
            return;
        }

        const payload = {
            Gender: student.gender,
            Age: Number(student.age),
            Department: student.department,
            Attendance: Number(student.attendance),
            Midterm_Score: Number(student.midterm),
            Assignments_Avg: Number(student.assignments),
            Quizzes_Avg: Number(student.quizzes),
            Participation_Score: Number(student.participation),
            Projects_Score: Number(student.projects),
            Study_Hours_per_Week: Number(student.studyHours),
            Extracurricular_Activities: student.extracurricular === 'Yes' ? 'Yes' : 'No',
            Internet_Access_at_Home: student.internetAccess === 'Yes' ? 'Yes' : 'No',
            Parent_Education_Level: student.parentEducation,
            Stress_Level: Number(student.stressLevel),
            Sleep_Hours_per_Night: Number(student.sleepHours),
        };

        try {
            const res = await fetch(`${BACKEND_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const data = await res.json();
            setResults([data]);
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        } catch (err) {
            setResults([{ error: 'Failed to fetch prediction.' }]);
        }
    };

    const textFields = [
        ['age', 'Age', 'number'],
        ['attendance', 'Attendance (%)', 'number'],
        ['midterm', 'Midterm Score', 'number'],
        ['assignments', 'Assignments Avg', 'number'],
        ['quizzes', 'Quizzes Avg', 'number'],
        ['participation', 'Participation Score', 'number'],
        ['projects', 'Projects Score', 'number'],
        ['studyHours', 'Study Hours/Week', 'number'],
        ['stressLevel', 'Stress Level (1-10)', 'number'],
        ['sleepHours', 'Sleep Hours/Night', 'number'],
    ];

    return (
        <div className="min-h-screen bg-gray-950 text-white p-4 sm:p-6">
            <h1 className="text-5xl font-bold text-lime-400 text-center mb-6">LearnLytics</h1>
            <div className="space-y-10">
                {students.map((student, idx) => (
                    <div key={idx} className="bg-gray-900 p-6 rounded-2xl shadow-lg max-w-4xl mx-auto">
                        <h2 className="text-xl font-semibold text-lime-300 mb-4">Enter Student Details</h2>

                        <div className="grid grid-cols-1 sm:grid-cols-1 gap-4">
                            <div>
                                <label className="block text-sm mb-1">Gender</label>
                                <select
                                    name="gender"
                                    value={student.gender}
                                    onChange={(e) => handleChange(idx, e)}
                                    className="w-full px-3 py-2 bg-gray-800 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-lime-400"
                                >
                                    <option value="">Select Gender</option>
                                    {genders.map((gender) => (
                                        <option key={gender} value={gender}>{gender}</option>
                                    ))}
                                </select>
                            </div>

                            {textFields.map(([name, label, type]) => (
                                <div key={name}>
                                    <label className="block text-sm mb-1">{label}</label>
                                    <input
                                        type={type}
                                        name={name}
                                        value={student[name]}
                                        onChange={(e) => handleChange(idx, e)}
                                        className="w-full px-3 py-2 bg-gray-800 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-lime-400"
                                        min={name === 'stressLevel' ? "1" : (name === 'sleepHours' ? "0" : "0")}
                                        max={name === 'stressLevel' ? "10" : (name === 'sleepHours' ? "24" : "100")}
                                    />
                                </div>
                            ))}

                            {[
                                ['department', 'Department', departments],
                                ['extracurricular', 'Extracurricular Activities', ['Yes', 'No']],
                                ['internetAccess', 'Internet Access at Home', ['Yes', 'No']],
                                ['parentEducation', 'Parent Education Level', parentEducationOptions],
                            ].map(([name, label, options]) => (
                                <div key={name}>
                                    <label className="block text-sm mb-1">{label}</label>
                                    <select
                                        name={name}
                                        value={student[name]}
                                        onChange={(e) => handleChange(idx, e)}
                                        className="w-full px-3 py-2 bg-gray-800 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-lime-400"
                                    >
                                        <option value="">Select</option>
                                        {typeof options[0] === 'object' ? (
                                            options.map((opt) => (
                                                <option key={opt.value} value={opt.value}>{opt.label}</option>
                                            ))
                                        ) : (
                                            options.map((opt) => (
                                                <option key={opt} value={opt}>{opt}</option>
                                            ))
                                        )}
                                    </select>
                                </div>
                            ))}
                        </div>

                        <div className="mt-6 flex justify-center">
                            <button
                                onClick={handleSubmit}
                                className="bg-lime-600 hover:bg-lime-700 text-white py-2 px-7 rounded-xl"
                            >
                                Submit
                            </button>
                        </div>
                    </div>
                ))}

                {results.length > 0 && (
                    <div className="mt-10 bg-gray-900 p-6 rounded-2xl shadow-lg max-w-4xl mx-auto">
                        <h2 className="text-2xl font-bold text-lime-300 mb-6 text-center">Predicted Results</h2>
                        <div className="grid gap-4">
                            {results.map((res, idx) => (
                                <div
                                    key={idx}
                                    className="bg-gray-800 border border-lime-600 rounded-xl p-5 text-white shadow-md"
                                >
                                    {res.error ? (
                                        <p className="text-red-400">{res.error}</p>
                                    ) : (
                                        <ul className="space-y-2 text-sm px-4">
                                            {Object.entries(res).map(([key, value]) => (
                                                <li key={key} className="flex justify-between border-b border-gray-700 pb-1">
                                                    <span className="capitalize text-gray-300">{key.replace(/_/g, ' ')}:</span>
                                                    <span className="text-lime-300 font-medium">{value.toString()}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default LearnLyticsForm;
