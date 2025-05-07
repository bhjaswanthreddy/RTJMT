'use client';

import React, { useEffect, useState, useMemo } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line
} from 'recharts';
import jobData from '../data/jobData.json';
import { Briefcase, Users, MapPin, Info } from 'lucide-react';
import dayjs from 'dayjs';
import Select from 'react-select';

const tabs = [
  { name: 'Dashboard', icon: <Briefcase size={16} />, id: 'dashboard' },
  { name: 'Analytics', icon: <Users size={16} />, id: 'analytics' },
  { name: 'Skill Match', icon: <MapPin size={16} />, id: 'skill' },
  { name: 'Resume Matcher', icon: <Briefcase size={16} />, id: 'resume' },
  { name: 'About', icon: <Info size={16} />, id: 'about' },
];

const customStyles = {
  control: (base) => ({
    ...base,
    backgroundColor: '#2a2a3c',
    borderColor: '#4b5563',
    color: 'white',
  }),
  menu: (base) => ({
    ...base,
    backgroundColor: '#2a2a3c',
    color: 'white',
  }),
  option: (base, state) => ({
    ...base,
    backgroundColor: state.isFocused ? '#4b5563' : '#2a2a3c',
    color: 'white',
  }),
  multiValue: (base) => ({
    ...base,
    backgroundColor: '#6b7280',
    color: 'white',
  }),
  multiValueLabel: (base) => ({
    ...base,
    color: 'white',
  }),
  multiValueRemove: (base) => ({
    ...base,
    color: 'white',
    ':hover': {
      backgroundColor: '#ef4444',
      color: 'white',
    },
  }),
};

export default function Page() {
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [filteredData, setFilteredData] = useState(jobData);
  const [selectedSkills, setSelectedSkills] = useState([]);
  const [location, setLocation] = useState('');
  const [experience, setExperience] = useState('');

  const [currentPage, setCurrentPage] = useState(1);
const jobsPerPage = 15;

const totalPages = Math.ceil(filteredData.length / jobsPerPage);
const paginatedJobs = filteredData.slice((currentPage - 1) * jobsPerPage, currentPage * jobsPerPage);

// Reset to page 1 when filters change
useEffect(() => {
  setCurrentPage(1);
}, [selectedSkills, location, experience]);


  const allSkills = Array.from(
    new Set(jobData.flatMap(job => job.Skills?.split(',').map(s => s.trim()) || []))
  );
  const skillOptions = allSkills.map(skill => ({ label: skill, value: skill }));
  const allLocations = Array.from(new Set(jobData.map(job => job.Location)));
  const allExperiences = Array.from(new Set(jobData.map(job => job.Experience_Level)));

  useEffect(() => {
    let data = [...jobData];

    if (selectedSkills.length > 0) {
      data = data.filter(job =>
        selectedSkills.every(skill =>
          job.Skills?.toLowerCase().includes(skill.toLowerCase())
        )
      );
    }

    if (location) {
      data = data.filter((job) => job.Location === location);
    }

    if (experience) {
      data = data.filter((job) => job.Experience_Level === experience);
    }

    setFilteredData(data);
  }, [selectedSkills, location, experience]);

  const avgSalary = Math.round(filteredData.reduce((sum, job) => sum + Number(job.Salary_USD), 0) / filteredData.length || 0);
  const topLocation = Object.entries(filteredData.reduce((acc, job) => {
    acc[job.Location] = (acc[job.Location] || 0) + 1;
    return acc;
  }, {})).sort((a, b) => b[1] - a[1])[0]?.[0];

  const jobCounts = filteredData.reduce((acc, job) => {
    acc[job.Job_Title] = (acc[job.Job_Title] || 0) + 1;
    return acc;
  }, {});
  const chartData = Object.entries(jobCounts).map(([title, count]) => ({ name: title, jobs: count }));

  const salaryByLocation = Object.entries(filteredData.reduce((acc, job) => {
    if (!acc[job.Location]) acc[job.Location] = [];
    acc[job.Location].push(job.Salary_USD);
    return acc;
  }, {})).map(([location, salaries]) => ({
    location,
    avg: Math.round(salaries.reduce((a, b) => a + b, 0) / salaries.length)
  }));

  const salaryByTitle = Object.entries(filteredData.reduce((acc, job) => {
    if (!acc[job.Job_Title]) acc[job.Job_Title] = [];
    acc[job.Job_Title].push(job.Salary_USD);
    return acc;
  }, {})).map(([title, salaries]) => ({
    title,
    avg: Math.round(salaries.reduce((a, b) => a + b, 0) / salaries.length)
  }));

  const salaryByMonth = useMemo(() => {
    const grouped = filteredData.reduce((acc, job) => {
      const month = dayjs(job.Date_Posted).format('YYYY-MM');
      if (!acc[month]) acc[month] = [];
      acc[month].push(Number(job.Salary_USD));
      return acc;
    }, {});
    return Object.entries(grouped)
      .map(([month, salaries]) => ({
        month,
        avg: Math.round(salaries.reduce((a, b) => a + b, 0) / salaries.length)
      }))
      .sort((a, b) => a.month.localeCompare(b.month));
  }, [filteredData]);

  const minSalary = Math.min(...salaryByMonth.map(d => d.avg));
  const maxSalary = Math.max(...salaryByMonth.map(d => d.avg));

  return (
    <main className="min-h-screen bg-[#1e1e2f] text-white p-6">
      <header className="flex flex-col items-center mb-6 text-center">
        <h1 className="text-2xl font-bold mb-4">Cloud Architect Job Market Analysis</h1>
        <div className="space-x-4 flex flex-wrap justify-center">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id)}
              className={`px-4 py-2 rounded-full flex items-center gap-2 text-sm font-medium transition duration-300
                ${selectedTab === tab.id ? 'bg-purple-600 text-white' : 'bg-[#2a2a3c] text-gray-300 hover:bg-purple-700 hover:text-white'}`}
            >
              {tab.icon} {tab.name}
            </button>
          ))}
        </div>
      </header>

      {selectedTab === 'dashboard' && (
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-[#2a2a3c] p-6 rounded-xl shadow-md">
            <h3 className="text-gray-400 text-sm uppercase mb-1">Total Jobs</h3>
            <p className="text-3xl font-bold">{filteredData.length}</p>
          </div>
          <div className="bg-[#2a2a3c] p-6 rounded-xl shadow-md">
            <h3 className="text-gray-400 text-sm uppercase mb-1">Avg Salary (USD)</h3>
            <p className="text-3xl font-bold">${avgSalary.toLocaleString()}</p>
          </div>
          <div className="bg-[#2a2a3c] p-6 rounded-xl shadow-md">
            <h3 className="text-gray-400 text-sm uppercase mb-1">Top Location</h3>
            <p className="text-3xl font-bold">{topLocation}</p>
          </div>
          <div className="col-span-full bg-[#2a2a3c] p-6 rounded-xl shadow-md">
            <h3 className="text-lg font-semibold mb-4">Jobs by Title</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={chartData}>
                <XAxis dataKey="name" stroke="#ccc" />
                <YAxis stroke="#ccc" />
                <Tooltip />
                <Bar dataKey="jobs" fill="#a78bfa" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      )}

      {selectedTab === 'analytics' && (
        <section className="grid grid-cols-1 gap-6">
          <div className="flex flex-wrap gap-4 mb-6">
            <div className="w-full md:w-64">
              <Select
                isMulti
                options={skillOptions}
                value={selectedSkills.map(skill => ({ label: skill, value: skill }))}
                onChange={(selected) => setSelectedSkills(selected.map(item => item.value))}
                placeholder="Select Skills"
                styles={customStyles}
              />
            </div>

            <select value={experience} onChange={e => setExperience(e.target.value)} className="bg-gray-800 text-white p-2 rounded">
              <option value="">Experience</option>
              {allExperiences.map(level => <option key={level}>{level}</option>)}
            </select>

            <select value={location} onChange={e => setLocation(e.target.value)} className="bg-gray-800 text-white p-2 rounded">
              <option value="">Location</option>
              {allLocations.map(loc => <option key={loc}>{loc}</option>)}
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-[#2a2a3c] p-6 rounded-xl shadow-md">
              <h3 className="text-lg font-semibold mb-4">Avg Salary by Job Title</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={salaryByTitle}>
                  <XAxis dataKey="title" stroke="#ccc" angle={-25} interval={0} height={70} tick={{ fontSize: 12 }} textAnchor="end" />
                  <YAxis stroke="#ccc" />
                  <Tooltip />
                  <Bar dataKey="avg" fill="#60a5fa" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="bg-[#2a2a3c] p-6 rounded-xl shadow-md">
              <h3 className="text-lg font-semibold mb-4">Avg Salary by Location</h3>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={salaryByLocation}>
                  <XAxis dataKey="location" stroke="#ccc" angle={-25} interval={0} height={70} tick={{ fontSize: 12 }} textAnchor="end" />
                  <YAxis stroke="#ccc" />
                  <Tooltip />
                  <Bar dataKey="avg" fill="#34d399" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="col-span-full bg-[#2a2a3c] p-6 rounded-xl shadow-md">
              <h3 className="text-lg font-semibold mb-4">Salary Trend Over Time</h3>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={salaryByMonth}>
                  <XAxis dataKey="month" stroke="#ccc" />
                  <YAxis stroke="#ccc" domain={[minSalary, maxSalary]} />
                  <Tooltip formatter={(value) => `$${value}`} />
                  <Line type="monotone" dataKey="avg" stroke="#a78bfa" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>
      )}
      {selectedTab === 'skill' && (
  <section>
    <h2 className="text-xl font-semibold mb-4">Skill Match & Job Recommendations</h2>

    <div className="flex flex-wrap gap-4 mb-6">
      <Select
        isMulti
        options={skillOptions}
        value={selectedSkills.map(skill => ({ label: skill, value: skill }))}
        onChange={(selected) => setSelectedSkills(selected.map(item => item.value))}
        placeholder="Select Skills"
        className="text-black w-64"
      />
      <select value={experience} onChange={e => setExperience(e.target.value)} className="bg-gray-800 text-white p-2 rounded">
        <option value="">Experience</option>
        {allExperiences.map(level => <option key={level}>{level}</option>)}
      </select>
      <select value={location} onChange={e => setLocation(e.target.value)} className="bg-gray-800 text-white p-2 rounded">
        <option value="">Location</option>
        {allLocations.map(loc => <option key={loc}>{loc}</option>)}
      </select>
    </div>

    <div className="bg-[#2a2a3c] p-6 rounded-xl shadow-md">
      <h3 className="text-lg font-semibold mb-4">
        Recommended Jobs <span className="text-sm text-gray-400">({filteredData.length} jobs found)</span>
      </h3>

      {paginatedJobs.length > 0 ? (
        <>
          <ul className="space-y-4">
            {paginatedJobs.map((job, idx) => (
              <li key={idx} className="bg-[#1e1e2f] p-4 rounded-lg border border-gray-700">
                <p className="font-bold text-white">{job.Job_Title}</p>
                <p className="text-sm text-gray-400">{job.Company} • {job.Location}</p>
                <p className="text-sm text-gray-400">💰 ${job.Salary_USD} • {job.Experience_Level}</p>
                <p className="text-sm text-gray-400">Skills: {job.Skills}</p>
              </li>
            ))}
          </ul>

          <div className="flex justify-between items-center mt-6 text-sm text-gray-300">
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="bg-purple-700 px-4 py-1 rounded disabled:opacity-50"
            >
              Previous
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="bg-purple-700 px-4 py-1 rounded disabled:opacity-50"
            >
              Next
            </button>
          </div>
        </>
      ) : (
        <p className="text-gray-400">No matching jobs found. Try adjusting your filters.</p>
      )}
    </div>
  </section>
)}



      {selectedTab === 'about' && (
        <section className="max-w-3xl mx-auto bg-[#2a2a3c] p-8 rounded-xl shadow-md">
          <h2 className="text-2xl font-bold mb-4 text-white">About This Project</h2>
          <p className="text-gray-300 leading-relaxed">
            This interactive dashboard was built to analyze the job market and salary trends for Cloud Architect roles.
            It includes dynamic insights on salary distributions, skill demand, and personalized job recommendations.
          </p>
          <ul className="mt-4 text-sm text-gray-400 space-y-2">
            <li>🔍 Built with <strong>React</strong>, <strong>Tailwind CSS</strong>, and <strong>Recharts</strong></li>
            <li>📊 Visualized using <strong>real-world job data</strong></li>
            <li>💻 Designed for career guidance and benchmarking</li>
          </ul>
          <div className="mt-6 text-sm text-gray-500 italic">
            Developed by Team 20 • Final Year Capstone Project
          </div>
        </section>

      )}
      {selectedTab === 'resume' && (
  <section className="max-w-3xl mx-auto bg-[#2a2a3c] p-8 rounded-xl shadow-md">
    <h2 className="text-2xl font-bold mb-4 text-white">Resume Matcher</h2>
    <p className="text-gray-300 mb-4">Upload your resume to see which skills match available jobs.</p>

    <input
      type="file"
      accept=".txt,.pdf"
      onChange={async (e) => {
        const file = e.target.files?.[0];
        if (!file) return;

        const text = await file.text();
        const matchedSkills = allSkills.filter(skill =>
          text.toLowerCase().includes(skill.toLowerCase())
        );

        setSelectedSkills(matchedSkills); // Update selected skills

        const resumeJobs = jobData.filter(job =>
          matchedSkills.every(skill =>
            job.Skills?.toLowerCase().includes(skill.toLowerCase())
          )
        );

        setFilteredData(resumeJobs);
        setSelectedTab('skill'); // Redirect to Skill Match tab
      }}
      className="mb-4 p-2 bg-gray-800 text-white rounded"
    />

    <p className="text-sm text-gray-400">Accepted formats: .txt, .pdf (text-only PDFs)</p>

    {selectedSkills.length > 0 && (
      <div className="mt-4">
        <h3 className="text-lg font-semibold text-white mb-2">Matched Skills:</h3>
        <p className="text-gray-300">{selectedSkills.join(', ')}</p>
      </div>
    )}
  </section>
)}



    </main>
  );
}
