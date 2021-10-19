import { PropTypes } from 'prop-types';

const Header = ({title}) => {
    return (
        <header className='header'>
            <h1 style={headingStyle}>{title}</h1>
            <button className='btn'>Add</button>
        </header>
    )
}

Header.defaultProps = {
    title: 'COVID Tracker',
}

Header.propTypes = {
    title: PropTypes.string,
}

const headingStyle = {
    color: 'red',
    background: 'black',
}

export default Header