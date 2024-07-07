import './Second.css';
import { useNavigate } from 'react-router-dom';

function Second() {
    const navigate = useNavigate();

    const fetchWhereToEat = async (whereToEat) => {
        let result = await fetch('http://127.0.0.1:5000/api/start/' + whereToEat)
        .then(response => response.json());
        console.log(result)
        return result.order_num;
    }

    const takeOut = async () => {
        let ordernum = await fetchWhereToEat('takeOut');
        navigate('/menu?id=' + ordernum);
    };
    const eatIn = async () => {
        let ordernum = await fetchWhereToEat('eatIn');
        navigate('/menu?id=' + ordernum);
    };

    return (
        <div className='total'>
            <button className='takeOut' onClick={takeOut}>포장</button><br/>
            <button className='eatIn' onClick={eatIn}>매장</button>
        </div>
    );
    }


export default Second;