import './Second.css';
import { useNavigate } from 'react-router-dom';

function Second() {
    const navigate = useNavigate();
    const takeOut = () => {
        navigate('/menu?whereToEat=포장');
    };
    const eatIn = () => {
        navigate('/menu?whereToEat=매장');
    };
    return (
        <div className='total'>
            <button className='takeOut' onClick={takeOut}>포장</button><br/>
            <button className='eatIn' onClick={eatIn}>매장</button>
        </div>
    );
}

export default Second;