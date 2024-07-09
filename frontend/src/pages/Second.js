import './Second.css';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { getSpeech } from '../util/GetSpeech';

function Second() {
    const navigate = useNavigate();
    const [load, setLoad] = useEffect(false);

    const fetchWhereToEat = async (whereToEat) => {
        let result = await fetch('http://127.0.0.1:5000/api/start/' + whereToEat)
        .then(response => response.json());
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

    useEffect(() => {
        window.speechSynthesis.getVoices();
        setLoad(true);
    }, []);

    useEffect(() => {
        getSpeech('포장하실지, 매장에서 드실지 선택해주세요.');
    }, [load]);

    return (
        <div className='total'>
            <button className='takeOut' onClick={takeOut}>포장</button><br/>
            <button className='eatIn' onClick={eatIn}>매장</button>
        </div>
    );
    }


export default Second;