import Header from "./Header";
import { useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import './HowToPay.css';
import getSpeech from "../util/GetSpeech";

function HowToPay() {
    const [searchParams] = useSearchParams();
    const [whereToEat, setWhereToEat] = useState('');
    const id = searchParams.get('id');
    const navigate = useNavigate();

    const fetchId = async () => {
        await fetch('http://127.0.0.1:5000/api/getinfo/' + id)
        .then(response => response.json())
        .then(data => {
            setWhereToEat(data.wheretoeat);
        });
    };

    const pay = () => {
        navigate('/pay?id=' + id);
    }

    const point = () => {
        navigate('/point?id=' + id);
    }

    const coupon = () => {
        navigate('/coupon?id=' + id);
    }

    const cancel = () => {
        navigate('/menu?id=' + id);
    };

    useEffect(() => {
        fetchId();
        getSpeech('결제 방법을 선택해주세요.');
    }, []);

    return (
        <>
            <Header whereToEat={whereToEat}/>
            <div className="payButtonDiv">
                <button className="payNow" onClick={() => {pay()}}>바로 결제</button>
                <button className="point" onClick={() => {point()}}>포인트 적립</button>
                <button className="coupon" onClick={() => {coupon()}}>쿠폰 사용</button>
            </div>
            <footer className='footer2'>
                <button className='cancelButton2' onClick={() => {cancel()}}>이전으로</button>
            </footer>
        </>
    );
}

export default HowToPay;