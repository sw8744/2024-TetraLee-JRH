import './Receipt.css';
import { useState } from 'react';
import Header from './Header';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useEffect } from 'react';

function Receipt() {
    const [number, setNumber] = useState(0);
    const [searchParams] = useSearchParams();
    const id = searchParams.get('id');
    const [whereToEat, setWhereToEat] = useState('');
    const nagivate = useNavigate();

    const fetchId = async () => {
        fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
            setNumber(data.id);
        });
    };

    const moveToMain = () => {
        nagivate('/');
    };

    useEffect(() => {
        fetchId();
    }, []);

    return (
        <>
            <Header whereToEat={whereToEat}/>
            <div>
                <p className='finishPay'>결제가 완료되었습니다.<br/></p>
                <p className='receipt'>영수증을</p>
                <p className='receipt'>출력하시겠습니까?</p>
            </div>
            <div className='yesNoButtonDiv'>
                <button className='yesButton' onClick={() => {moveToMain()}}>예</button>
                <button className='noButton' onClick={() => {moveToMain()}}>아니오</button>
            </div>
            <div className='numberDiv'>
                <p className='number'>주문 번호 {number}번</p>
            </div>
        </>
    );
}

export default Receipt;