
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../../components/Navbar";
import Loader from "../../components/Loader";
import { getAllDoctors } from "../../services/patient.service";

export default function RecommendedDoctors() {
  const navigate = useNavigate();
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDoctors();
  }, []);

  const loadDoctors = async () => {
    try {
      const res = await getAllDoctors();
      setDoctors(res.data);
    } catch (err) {
      console.error("Error loading doctors:", err);
      setError("Failed to load doctors. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="flex justify-center items-center min-h-screen">
          <Loader />
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Recommended Doctors</h1>
            <p className="text-gray-600">Find and book appointments with qualified healthcare professionals</p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          {doctors.length === 0 && !error && (
            <div className="bg-white rounded-lg shadow-md p-8 text-center">
              <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <h3 className="mt-2 text-lg font-medium text-gray-900">No doctors available</h3>
              <p className="mt-1 text-sm text-gray-500">Check back later for available doctors.</p>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {doctors.map((doctor) => (
              <div 
                key={doctor.id} 
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden"
              >
                <div className="p-6">
                  {/* Doctor Avatar */}
                  <div className="flex items-center mb-4">
                    <div className="flex-shrink-0">
                      {doctor.profile_picture ? (
                        <img 
                          src={doctor.profile_picture} 
                          alt={doctor.username}
                          className="h-16 w-16 rounded-full object-cover"
                        />
                      ) : (
                        <div className="h-16 w-16 rounded-full bg-brand-red flex items-center justify-center">
                          <span className="text-2xl font-bold text-white">
                            {doctor.username?.charAt(0).toUpperCase() || 'D'}
                          </span>
                        </div>
                      )}
                    </div>
                    <div className="ml-4">
                      <h3 className="text-lg font-semibold text-gray-900">
                        Dr. {doctor.username || doctor.first_name} {doctor.last_name}
                      </h3>
                      {doctor.specialization && (
                        <p className="text-sm text-brand-red font-medium">{doctor.specialization}</p>
                      )}
                    </div>
                  </div>

                  {/* Doctor Info */}
                  <div className="space-y-2 mb-4">
                    {doctor.email && (
                      <div className="flex items-center text-sm text-gray-600">
                        <svg className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                        {doctor.email}
                      </div>
                    )}

                    {doctor.phone_number && (
                      <div className="flex items-center text-sm text-gray-600">
                        <svg className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                        </svg>
                        {doctor.phone_number}
                      </div>
                    )}

                    {doctor.bio && (
                      <p className="text-sm text-gray-600 mt-3 line-clamp-3">
                        {doctor.bio}
                      </p>
                    )}
                  </div>

                  {/* Experience/Rating (if available) */}
                  {(doctor.years_of_experience || doctor.rating) && (
                    <div className="flex items-center gap-4 mb-4 pt-4 border-t border-gray-200">
                      {doctor.years_of_experience && (
                        <div className="text-sm">
                          <span className="font-semibold text-gray-900">{doctor.years_of_experience}</span>
                          <span className="text-gray-600"> years exp.</span>
                        </div>
                      )}
                      {doctor.rating && (
                        <div className="flex items-center text-sm">
                          <svg className="h-4 w-4 text-yellow-400 mr-1" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                          </svg>
                          <span className="font-semibold text-gray-900">{doctor.rating}</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Action Buttons */}
                  <div className="flex gap-3">
                    <button
                      onClick={() => navigate(`/patient/book?doctor=${doctor.id}`)}
                      className="flex-1 btn-primary text-sm py-2"
                    >
                      Book Appointment
                    </button>
                    <button
                      onClick={() => navigate(`/patient/doctor/${doctor.id}`)}
                      className="px-4 py-2 text-sm border border-brand-red text-brand-red rounded-lg hover:bg-brand-red hover:text-white transition-colors"
                    >
                      View Profile
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}