import React, {useState, useEffect} from 'react'
import TemporaryDrawer from '../components/TemporaryDrawer';
import TotalsTable from '../components/TotalsTable';

export const Informative = () => {
    const [loading, setLoading] = useState(false);
    const [main, setMain] = useState([]);
    // Fips codes for counties we currently support
    const [counties] = useState([44001, 44003, 44005, 44007, 44009]);

    useEffect(() => {
        // Load county data
        Promise.all(counties.map(fips =>
            fetch(`http://localhost:5000/county/${fips}`)
                .then(response => response.json())
        )).then(data => {
            // Replace state id with state name
            var id_val = 0;

            for (let county of data) {
                if (county.state_id === 44) {
                    county.state = 'Rhode Island';
                    county.id = id_val++;
                }
            }
            setMain(data);
            setLoading(true);
        });
    }, [counties]);

    return (
        <div>
            {!loading ? <div>Loading....</div> : <div>
            <TemporaryDrawer/>
            <TotalsTable data={main} />
            </div>}
        </div>
    )
}

export default Informative;
