(define (problem blocksworld-6)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear f)
    (clear d)
    (handempty)
    (on f e)
    (on e b)
    (on d a)
    (on a c)
    (ontable b)
    (ontable c)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
