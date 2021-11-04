import React , {useEffect, useState} from 'react'

export const CustomPopup = ({ fips }) => {
    const [saved_data,setData] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/county/' + String(fips), {
            headers : { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }).then(response=>response.json())
        .then(data => {
            setData(data);
        });
    },[fips])

    return (
        <div>
            Total Cases: {saved_data.total_cases}<br/>
            Total Deaths: {saved_data.total_deaths}<br/>
            Total Hospitalizations: {saved_data.total_hospital}<br/>
            Total Vaccinations: {saved_data.total_vaccinated}
        </div>
    )
}

